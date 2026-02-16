from fastapi import FastAPI, HTTPException
from fastapi.responses import Response, FileResponse
from PyPDF2 import PdfReader

from .models import OrderRequest
from .pdf_engine import paginate_two_per_page, build_overlay_pdf, merge_overlay_with_background
from .template_config import CONFIGS

app = FastAPI(title="App de Rótulos - Anclajes / Pernos")

@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs", "ui": "/rotulos"}

@app.get("/rotulos")
def rotulos_ui():
    return FileResponse("static/rotulos.html")

MAX_ITEMS = 500

@app.post("/generate-pdf")
def generate_pdf(payload: OrderRequest):
    if len(payload.items) > MAX_ITEMS:
        raise HTTPException(
            status_code=400,
            detail=f"Demasiados rótulos: {len(payload.items)}. Máximo permitido: {MAX_ITEMS}."
        )

    cfg = CONFIGS[payload.producto]

    if payload.producto == "anclajes":
        bg_path = "templates/anclajes_bg.pdf"
        get_cables_o_perno = lambda it: str(it.cables)
    else:
        bg_path = "templates/pernos_bg.pdf"
        get_cables_o_perno = lambda it: it.tipo_perno

    bg_reader = PdfReader(bg_path)
    mb = bg_reader.pages[0].mediabox
    page_size = (float(mb.width), float(mb.height))

    n = len(payload.items)
    stickers = []
    for idx, it in enumerate(payload.items, start=1):
        total = float(it.bulbo) + float(it.largo) + float(it.sobrelargo)
        stickers.append({
            "cliente": payload.cliente,
            "obra": payload.obra,
            "of": payload.of,
            "colada": payload.colada,

            "unidad": f"{idx}/{n}",
            "punto": it.punto,
            "inyeccion": it.inyeccion,
            "cables_o_perno": get_cables_o_perno(it).strip().upper(),

            "bulbo": float(it.bulbo),
            "largo": float(it.largo),
            "sobrelargo": float(it.sobrelargo),
            "total": total,
        })

    pages = paginate_two_per_page(stickers)
    overlay = build_overlay_pdf(pages, page_size, cfg)
    final_pdf = merge_overlay_with_background(overlay, bg_path)

    filename = f"{payload.producto}_{payload.of}_{payload.obra}".replace(" ", "_") + ".pdf"
    return Response(
        content=final_pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )