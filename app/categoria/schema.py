from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    descripcion: str = Field(..., min_length=2)


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    pass


class CategoriaRead(CategoriaBase):
    id: int
    fecha_creacion: datetime
    fecha_ultima_modificacion: Optional[datetime] = None
    usuario_ultima_modificacion: Optional[str] = None

    class Config:
        from_attributes = True
