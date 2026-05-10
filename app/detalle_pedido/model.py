from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

# Nuevamente, TYPE_CHECKING previene imports circulares:
if TYPE_CHECKING:
    from app.pedido.model import Pedido
    from app.producto.model import Producto


# Definimos la clase heredando de SQLModel, creamos la tabla:
class DetallePedido(SQLModel, table=True):
    __tablename__ = "detalle_pedido"

    # Los detalles de pedido tiene un PK compuesta con las 2 FK (tabla intermedia),
    # y también tienen una cantidad (refleja la cantidad de el producto X en el pedido),
    # así como el precio_unitario al que se "vendió" cada una unidad.
    pedido_id: int = Field(foreign_key="pedidos.id", primary_key=True)
    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    cantidad: int
    # Hay que guardar cuanto salía el producto al momento del pedido
    precio_unitario: float

    # Establecemos la relación con el pedido (al que corresponde el detalle)
    # y el producto que está "detallado".
    # Vincularemos bidireccionalmente pero no pondremos cascade_deletes.
    pedido: "Pedido" = Relationship(back_populates="lista_detalles")
    # Acá no va cascade_delete, porque si borramos un detalle no necesariamente
    # vamos a querer borrar todo el pedido (cancelan unas papas, o se equivocan
    # al comandar y ponen algo extra).
    producto: "Producto" = Relationship(back_populates="detalles")
    # Jamás podría tener cascade_delete, porque borrar un detalle no borra
    # el producto, y borrar un producto no puede destruir todos los detalles
    # de las ventas pasadas.
