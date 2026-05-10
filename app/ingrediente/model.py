from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

# Nuevamente, usamos TYPE_CHECKING para evitar importaciones circulares:
if TYPE_CHECKING:
    from app.producto_ingrediente.model import ProductoIngrediente


# Creamos un enum con strings para el atributo unidad_medida
class UnidadMedida(str, Enum):
    GRAMOS = "g"
    MILILITROS = "ml"
    UNIDAD = "u"


# Definimos Ingrediente heredando de SQLModel, pedimos que genera una tabla:
class Ingrediente(SQLModel, table=True):
    __tablename__ = "ingredientes"

    # Un ingrediente tiene un id, un nombre, descripción y una unidad de medida:
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, unique=True)
    descripcion: str = Field(max_length=200)
    unidad_de_medida: UnidadMedida
    alergeno: bool = Field(default=False)

    # Campos de auditoría:
    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    fecha_ultima_modificacion: Optional[datetime] = Field(default=None)
    usuario_ultima_modificacion: Optional[str] = Field(default=None)

    # Definimos la relación entre ingrediente y producto_ingrediente,
    # Está será representada con una tabla intermedia, y en este modelo
    # con una lista de objetos ProductoIngrediente:
    producto_ingrediente: List["ProductoIngrediente"] = Relationship(
        # back_populates vincula la relación con el atributo ingrediente
        # en el modelo producto_ingrediente de forma bidireccional.
        back_populates="ingrediente",
        # cascade_delete asegura que si se elimina el ingrediente
        # también se eliminarán los registros vinculados en la tabla intermedia.
        cascade_delete=True,
    )
