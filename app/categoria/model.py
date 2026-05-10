from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

# Al importar el modelo de ProductoCategoria, usamos
# TYPE_CHECKING para evitar importaciones circulares,
# porque ProductoCategoria también importa Categoría:
if TYPE_CHECKING:
    from app.producto_categoria.model import ProductoCategoria


# Definimos la clase heredando de SQLModel, le indicamos que
# genere una tabla al hacerlo:
class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    # Una categoría tiene un id, un nombre y una descripción,
    # la DB debe generar el campo id, por eso default=None y Optional:
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(
        max_length=100,
        unique=True,  # unico para no tener 2 categorías iguales
    )
    descripcion: str = Field(max_length=200)

    # Campos de auditoría:
    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    fecha_ultima_modificacion: Optional[datetime] = Field(default=None)
    usuario_ultima_modificacion: Optional[str] = Field(default=None)

    # Definimos la relación entre categoría y producto_categoría,
    # Está será representada con una tabla intermedia, y en este modelo
    # con una lista de objetos ProductoCategoría:
    producto_categoria: List["ProductoCategoria"] = Relationship(
        # back_populates vincula la relación con el atributo categoría
        # en el modelo producto_categoria de forma bidireccional.
        back_populates="categoria",
        # cascade_delete asegura que si se elimina la categoría
        # también se eliminarán los registros vinculados en la tabla intermedia.
        cascade_delete=True,
    )
