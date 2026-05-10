from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

# Nuevamente, usamos TYPE_CHECKING para evitar importaciones circulares:
if TYPE_CHECKING:
    from app.detalle_pedido.model import DetallePedido


# Creamos un enum con strings para el atributo estado:
class EstadoPedido(str, Enum):
    PENDIENTE = "pendiente"
    EN_PREPARACION = "en_preparacion"
    LISTO = "listo"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"


# Definimos Pedido heredando de SQLModel, creamos tabla:
class Pedido(SQLModel, table=True):
    __tablename__ = "pedidos"

    # Un pedido tiene un id, un estado y un cliente:
    id: Optional[int] = Field(default=None, primary_key=True)
    estado: EstadoPedido = Field(default=EstadoPedido.PENDIENTE)
    cliente: str = Field(max_length=100)

    # Campos de auditoría:
    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    fecha_ultima_modificacion: Optional[datetime] = Field(default=None)
    usuario_ultima_modificacion: Optional[str] = Field(default=None)

    # Definimos la relación entre pedido y detalle_pedido,
    # Está será representada con una tabla intermedia, y en este modelo
    # con una lista de objetos DetallePedido:
    lista_detalles: List["DetallePedido"] = Relationship(
        # back_populates vincula la relación con el atributo pedido
        # en el modelo detalle_pedido de forma bidireccional.
        back_populates="pedido",
        # cascade_delete asegura que si elimiamos el pedido,
        # se eliminen los registros vinculados en la tabla intermedia.
        cascade_delete=True,
    )
