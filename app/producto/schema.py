from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    descripcion: str = Field(..., min_length=2)
    precio_base: float = Field(..., gt=0)
    imagen_url: List[str] = Field(default_factory=list)
    disponible: bool = True


class ProductoCreate(ProductoBase):
    categoria_ids: List[int] = Field(default_factory=list)


class ProductoUpdate(ProductoBase):
    categoria_ids: List[int] = Field(default_factory=list)


class ProductoRead(ProductoBase):
    id: int
    fecha_creacion: datetime
    fecha_ultima_modificacion: Optional[datetime] = None
    usuario_ultima_modificacion: Optional[str] = None

    class Config:
        from_attributes = True
