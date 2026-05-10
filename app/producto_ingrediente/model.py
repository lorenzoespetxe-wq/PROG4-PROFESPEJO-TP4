from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

# Nuevamente, TYPE_CHECKING previene imports circulares:
if TYPE_CHECKING:
    from app.producto.model import Producto
    from app.ingrediente.model import Ingrediente


# Definimos la clase heredando de SQLModel, creamos la tabla:
class ProductoIngrediente(SQLModel, table=True):
    __tablename__ = "producto_ingrediente"

    # La relacion productoIngrediente tiene un PK compuesta con las 2 FK
    # (tabla intermedia), y también tienen una cantidad (refleja la cantidad de
    # un ingrediente que se usa para elaborar el producto):
    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    ingrediente_id: int = Field(foreign_key="ingredientes.id", primary_key=True)
    cantidad: float  # cantidad de el ingrediente que se usa para elborar el prod.

    # Establecemos la relación con el producto y el ingrediente,
    # la relación es bidireccional por posibles funcionalidades,
    # pero sin cascade_delete porque podrías matar la DB solo por
    # sacarle un ingrediente a una pizza.
    producto: "Producto" = Relationship(back_populates="producto_ingrediente")
    ingrediente: "Ingrediente" = Relationship(back_populates="producto_ingrediente")
