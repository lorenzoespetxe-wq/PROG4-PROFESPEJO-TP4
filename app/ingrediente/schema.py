from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from app.ingrediente.model import UnidadMedida


# BASE :
class IngredienteBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    descripcion: str = Field(..., min_length=2)
    unidad_de_medida: UnidadMedida
    alergeno: bool = Field(default=False)


# POST :
# Hereda directamente de IngredienteBase.
class IngredienteCreate(IngredienteBase):
    pass


# PUT / PATCH :
# Se hereda de BaseModel para evitar arrastrar requerimientos del Base.
# Igual que el POST, pero los campos son opcionales para permitir
# actualizaciones parciales.
class IngredienteUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2)
    descripcion: Optional[str] = Field(default=None, min_length=2)
    unidad_de_medida: Optional[UnidadMedida] = None
    alergeno: Optional[bool] = None


# GET :
# Trae adicionalmente a IngredienteBase el id
# y los campos de auditoria:
class IngredienteRead(IngredienteBase):
    id: int
    fecha_creacion: datetime
    fecha_ultima_modificacion: Optional[datetime] = None
    usuario_ultima_modificacion: Optional[str] = None

    # Esta configuración es necesaria para que pydantic lea
    # objetos python, en vez de diccionarios (x defecto).
    model_config = ConfigDict(from_attributes=True)
