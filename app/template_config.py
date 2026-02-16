from dataclasses import dataclass
from typing import Tuple, Dict, Literal

Point = Tuple[float, float]
ProductType = Literal["anclajes", "pernos"]

@dataclass(frozen=True)
class StickerFields:
    cliente: Point
    obra: Point
    unidad: Point
    punto: Point
    inyeccion: Point
    cables_o_perno: Point
    bulbo: Point
    largo: Point
    sobrelargo: Point
    total: Point
    of: Point
    colada: Point

@dataclass(frozen=True)
class LayoutConfig:
    top_origin: Point
    bottom_origin: Point
    font_name: str
    font_size: int
    fields: StickerFields

# =========================
# ANCLAJES (TU CONFIG YA PERFECTO)
# =========================
FIELDS_ANCLAJES = StickerFields(
    cliente=(115.5, 610.3),
    obra=(104.9, 587.8),

    unidad=(116.4, 565.4),
    inyeccion=(324.4, 565.4),
    cables_o_perno=(461.3, 565.4),

    punto=(458.0, 600.5),

    bulbo=(167.5, 545.8),
    largo=(239.1, 545.8),
    sobrelargo=(326.5, 545.8),
    total=(423.7, 545.8),

    of=(154.1, 520.4),
    colada=(381.7, 520.4),
)

CONFIG_ANCLAJES = LayoutConfig(
    top_origin=(0, 0),
    bottom_origin=(0, -321.47),
    font_name="Helvetica",
    font_size=10,
    fields=FIELDS_ANCLAJES,
)

# =========================
# PERNOS (PLACEHOLDER por ahora: genera PDF, luego calibramos)
# =========================
FIELDS_PERNOS = StickerFields(
    cliente=(115.5, 634.3),
    obra=(104.9, 611.8),

    unidad=(116.4, 589.4),
    inyeccion=(324.4, 589.4),
    cables_o_perno=(461.3, 589.4),  # aquí va el TIPO DE PERNO

    punto=(458.0, 624.5),

    bulbo=(167.5, 566.8),
    largo=(239.1, 566.8),
    sobrelargo=(326.5, 566.8),
    total=(423.7, 566.8),

    of=(154.1, 544.4),
    colada=(381.7, 544.4),
)

CONFIG_PERNOS = LayoutConfig(
    top_origin=(0, 0),
    bottom_origin=(0, -321.47),
    font_name="Helvetica",
    font_size=10,
    fields=FIELDS_PERNOS,
)

CONFIGS: Dict[ProductType, LayoutConfig] = {
    "anclajes": CONFIG_ANCLAJES,
    "pernos": CONFIG_PERNOS,
}