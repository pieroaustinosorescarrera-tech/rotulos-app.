import io
import copy
from typing import List, Dict, Tuple

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PyPDF2 import PdfReader, PdfWriter

from .template_config import LayoutConfig


def fmt2(x: float) -> str:
    return f"{x:.2f}"


def paginate_two_per_page(stickers: List[Dict]) -> List[List[Dict]]:
    pages: List[List[Dict]] = []
    for i in range(0, len(stickers), 2):
        pages.append(stickers[i:i + 2])
    return pages


def draw_sticker(c: canvas.Canvas, cfg: LayoutConfig, origin_x: float, origin_y: float, sticker: Dict):
    f = cfg.fields

    def put(pt, text):
        x, y = pt
        c.drawString(origin_x + x, origin_y + y, str(text))

    def put_center(pt, text):
        x, y = pt
        c.drawCentredString(origin_x + x, origin_y + y, str(text))

    # Constantes
    put(f.cliente, sticker["cliente"])
    put(f.obra, sticker["obra"])
    put(f.of, sticker["of"])
    put(f.colada, sticker["colada"])

    # Variables
    put(f.unidad, sticker["unidad"])

    # Punto: centrado + tamaño mayor, SIN negrita
    c.setFont(cfg.font_name, 14)
    put_center(f.punto, sticker["punto"])
    c.setFont(cfg.font_name, cfg.font_size)

    put(f.inyeccion, sticker["inyeccion"])
    put(f.cables_o_perno, sticker["cables_o_perno"])

    put(f.bulbo, fmt2(sticker["bulbo"]))
    put(f.largo, fmt2(sticker["largo"]))
    put(f.sobrelargo, fmt2(sticker["sobrelargo"]))
    put(f.total, fmt2(sticker["total"]))


def build_overlay_pdf(pages: List[List[Dict]], page_size: Tuple[float, float], cfg: LayoutConfig) -> bytes:
    """
    - Overlay del mismo tamaño que la hoja completa.
    - Si la página tiene SOLO 1 rótulo, blanquea la mitad inferior para ocultar el rótulo vacío.
    - Evita página extra: showPage() solo ENTRE páginas.
    """
    w, h = page_size

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=page_size)
    c.setFont(cfg.font_name, cfg.font_size)

    top_x, top_y = cfg.top_origin
    bot_x, bot_y = cfg.bottom_origin

    total_pages = len(pages)

    for idx, page in enumerate(pages):
        # Si SOLO hay 1 rótulo en esta hoja: blanquear la mitad inferior
        if len(page) == 1:
            c.saveState()
            c.setFillColor(colors.white)
            # Tapamos desde el borde inferior hasta un poco más de la mitad
            # para cubrir por completo el rótulo inferior del fondo.
            c.rect(0, 0, w, (h / 2.0) + 6, stroke=0, fill=1)
            c.restoreState()
            c.setFont(cfg.font_name, cfg.font_size)

        # Dibuja rótulo superior
        if len(page) >= 1:
            draw_sticker(c, cfg, top_x, top_y, page[0])

        # Dibuja rótulo inferior solo si existe (2 por hoja)
        if len(page) >= 2:
            draw_sticker(c, cfg, bot_x, bot_y, page[1])

        # IMPORTANTE: pasar página solo si NO es la última
        if idx < total_pages - 1:
            c.showPage()
            c.setFont(cfg.font_name, cfg.font_size)

    c.save()
    return buf.getvalue()


def merge_overlay_with_background(overlay_bytes: bytes, background_pdf_path: str) -> bytes:
    overlay_reader = PdfReader(io.BytesIO(overlay_bytes))
    bg_reader = PdfReader(background_pdf_path)

    bg_template = bg_reader.pages[0]

    writer = PdfWriter()
    for i in range(len(overlay_reader.pages)):
        base = copy.copy(bg_template)
        base.merge_page(overlay_reader.pages[i])
        writer.add_page(base)

    out = io.BytesIO()
    writer.write(out)
    return out.getvalue()