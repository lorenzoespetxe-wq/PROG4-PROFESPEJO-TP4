from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class DetallePedidoBase(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)


class DetallePedidoCreate(DetallePedidoBase):
    # No se incluye precio_unitario por seguridad; se obtiene del Producto en el Service
    pass


class DetallePedidoRead(DetallePedidoBase):
    precio_unitario: float
    producto_nombre: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
