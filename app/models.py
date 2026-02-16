from typing import List, Literal, Union
from pydantic import BaseModel, Field, field_validator, model_validator

ProductType = Literal["anclajes", "pernos"]

class ItemBase(BaseModel):
    punto: str = Field(..., min_length=1, max_length=32)
    inyeccion: str = Field(..., min_length=1, max_length=32)  # texto libre: IU/IR/IR1/etc.
    bulbo: float = Field(..., ge=0)
    largo: float = Field(..., ge=0)       # L. libre
    sobrelargo: float = Field(..., ge=0)

    @field_validator("punto")
    @classmethod
    def normalize_punto(cls, v: str) -> str:
        return v.strip()

    @field_validator("inyeccion")
    @classmethod
    def normalize_inyeccion(cls, v: str) -> str:
        return v.strip().upper()

class ItemAnclaje(ItemBase):
    cables: int = Field(..., ge=0, le=999)

class ItemPerno(ItemBase):
    tipo_perno: str = Field(..., min_length=1, max_length=64)

    @field_validator("tipo_perno")
    @classmethod
    def normalize_tipo_perno(cls, v: str) -> str:
        return v.strip().upper()

class OrderRequest(BaseModel):
    producto: ProductType
    cliente: str = Field(..., min_length=1, max_length=128)
    obra: str = Field(..., min_length=1, max_length=128)
    of: str = Field(..., min_length=1, max_length=64)
    colada: str = Field(..., min_length=1, max_length=64)
    items: List[Union[ItemAnclaje, ItemPerno]]

    @field_validator("cliente", "obra", "of", "colada")
    @classmethod
    def normalize_text(cls, v: str) -> str:
        return v.strip()

    @model_validator(mode="after")
    def validate_items_by_product(self):
        if len(self.items) == 0:
            raise ValueError("items no puede estar vacío.")

        if self.producto == "anclajes":
            for it in self.items:
                if not isinstance(it, ItemAnclaje):
                    raise ValueError("Para producto=anclajes, cada item debe incluir 'cables'.")
        else:
            for it in self.items:
                if not isinstance(it, ItemPerno):
                    raise ValueError("Para producto=pernos, cada item debe incluir 'tipo_perno'.")

        return self