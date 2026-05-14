from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# Sub-esquema necesario para capturar el ingrediente
# y la cantidad al crear la relación:
class ProductoIngredienteCreatePayload(BaseModel):
    ingrediente_id: int
    cantidad: float = Field(..., gt=0)


# BASE :
class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    descripcion: str = Field(..., min_length=2)
    precio_base: float = Field(..., gt=0)
    imagen_url: List[str] = Field(default_factory=list)
    disponible: bool = True


# POST :
class ProductoCreate(ProductoBase):
    # Recibe adicionalmente los IDs de las categorías:
    categoria_ids: List[int] = Field(default_factory=list)
    # Y el payload de ingredientes-cantidad:
    ingredientes: List[ProductoIngredienteCreatePayload] = Field(default_factory=list)


# PUT / PATCH :
# Se hereda de BaseModel para evitar arrastrar requerimientos del Base.
# Todos los default son explícitamente None.
class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2)
    descripcion: Optional[str] = Field(default=None, min_length=2)
    precio_base: Optional[float] = Field(default=None, gt=0)
    imagen_url: Optional[List[str]] = Field(default=None)
    disponible: Optional[bool] = None
    categoria_ids: Optional[List[int]] = Field(default=None)
    ingredientes: Optional[List[ProductoIngredienteCreatePayload]] = Field(default=None)


# GET :
# Trae adicionalmente a ProductoBase el id
# y los campos de auditoria:
class ProductoRead(ProductoBase):
    id: int
    fecha_creacion: datetime
    fecha_ultima_modificacion: Optional[datetime] = None
    usuario_ultima_modificacion: Optional[str] = None

    # Esta configuración es necesaria para que pydantic lea
    # objetos python, en vez de diccionarios (x defecto).
    model_config = ConfigDict(from_attributes=True)
