from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.pedido.model import EstadoPedido
from app.detalle_pedido.schema import DetallePedidoCreate, DetallePedidoRead


# BASE:
class PedidoBase(BaseModel):
    cliente: Optional[str] = Field(default=None, max_length=100)
    observaciones: Optional[str] = Field(default=None, max_length=200)


# POST:
class PedidoCreate(PedidoBase):
    # Un pedido no puede existir sin al menos un detalle (min_length=1)
    lista_detalles: List[DetallePedidoCreate] = Field(..., min_length=1)


# PUT/PATCH:
class PedidoUpdate(BaseModel):
    # Por regla de negocio, un pedido ya creado no debería permitir
    # modificar sus productos. Solo se actualiza su estado u observaciones.
    estado: Optional[EstadoPedido] = None
    observaciones: Optional[str] = Field(default=None, max_length=200)


# GET:
class PedidoRead(PedidoBase):
    id: int
    estado: EstadoPedido
    total: float  # Monto total calculado (sumatoria de detalles)
    fecha_creacion: datetime
    fecha_ultima_modificacion: Optional[datetime] = None
    usuario_ultima_modificacion: Optional[str] = None

    # Relación anidada: Devuelve la lista de productos comprados
    lista_detalles: List[DetallePedidoRead] = []

    model_config = ConfigDict(from_attributes=True)
