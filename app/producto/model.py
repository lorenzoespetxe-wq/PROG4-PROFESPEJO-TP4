from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON

# Nuevamente utilizamos TYPE_CHECKING para evitar imports circulares:
if TYPE_CHECKING:
    from app.producto_categoria.model import ProductoCategoria
    from app.producto_ingrediente.model import ProductoIngrediente


# Definimos la clase heredando de SQLModel, creamos la tabla:
class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    # Un producto tiene un id, un nombre (único), una descripción,
    # un precio de lista. También lleva imagenes, puede o no estar
    # disponible para la compra:
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(
        max_length=100,
        unique=True,  # unico para no tener 2 productos iguales
    )
    descripcion: str = Field(max_length=200)
    precio_base: float
    imagen_url: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    disponible: bool = Field(default=True)

    # Campos de auditoría:
    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    fecha_ultima_modificacion: Optional[datetime] = Field(default=None)
    usuario_ultima_modificacion: Optional[str] = Field(default=None)

    # Definimos las 2 relaciones N:N, con las tablas intermedias ProductoIngrediente
    # y ProductoCategoria.
    producto_ingrediente: List["ProductoIngrediente"] = Relationship(
        back_populates="producto", cascade_delete=True
    )
    producto_categoria: List["ProductoCategoria"] = Relationship(
        back_populates="producto", cascade_delete=True
    )
    # Nuevamente:
    # back_populates vincula la relación con el atributo respectivo
    # de las tablas intermedias.
    # cascade_delete=True, hace que si se elimina el producto,
    # no queden "huerfanos" los registros en las tablas intermedias.
