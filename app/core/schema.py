from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

# T es una variable de tipo genérica.
# Representa el payload (Categoria, Producto, Lista, etc.)
T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: str
    # data adopta el tipo que se le pase a 'T'.
    # Es Optional por si un DELETE no devuelve datos.
    data: Optional[T] = None
