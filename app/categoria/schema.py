from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


# BASE :
class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    descripcion: str = Field(..., min_length=2)


# POST :
# Hereda directamente de CategoriaBase.
class CategoriaCreate(CategoriaBase):
    pass


# PUT / PATCH :
# Se hereda de BaseModel para evitar arrastrar requerimientos del Base.
# Igual que el POST, pero los campos son opcionales para permitir
# actualizaciones parciales.
class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2)
    descripcion: Optional[str] = Field(default=None, min_length=2)


# GET :
# Trae adicionalmente a CategoriaBase el id
# y los campos de auditoria:
class CategoriaRead(CategoriaBase):
    id: int
    fecha_creacion: datetime
    fecha_ultima_modificacion: Optional[datetime] = None
    usuario_ultima_modificacion: Optional[str] = None

    # Esta configuración es necesaria para que pydantic lea
    # objetos python, en vez de diccionarios (x defecto).
    # Le dice...
    # lee: dato.nombre (python)
    # en vez de: dato["nombre"] (diccionario)
    model_config = ConfigDict(from_attributes=True)
