from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

# TYPE_CHEKING previene imports circulares:
if TYPE_CHECKING:
    from app.producto.model import Producto
    from app.categoria.model import Categoria


# Creamos la clase heredando de SQLModel, creamos la tabla:
class ProductoCategoria(SQLModel, table=True):
    __tablename__ = "producto_categoria"

    # Clave primaria compuesta por ambas FKs
    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categorias.id", primary_key=True)

    # Misma relación bidireccional que con el resto de las tablas intermedias,
    # sin cascade_delete, para que una desvinculación entre un producto_categoria
    # no nos rompa la DB:
    producto: Optional["Producto"] = Relationship(back_populates="producto_categoria")
    categoria: Optional["Categoria"] = Relationship(back_populates="producto_categoria")
