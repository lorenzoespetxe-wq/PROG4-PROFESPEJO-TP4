from typing import Generic, TypeVar, Optional
from pydantic import BaseModel


"""

Este código definirá un "Response Wrapper". Este es un patrón
de diseño de APIs REST que estandariza todas las peticiones que 
envía el back al front, para que tengan exactamente la misma forma
ya sea que la operación devuelva un objeto, una lista o nada.

Hace que el front siempre reciba un JSON predecible.

"""


# T es una variable de tipo genérica.
# Representa el payload (Categoria, Producto, Lista, etc.)
T = TypeVar("T")


# Definimos la clase RespuestaEstandart, que hereda de BaseModel
# y recibe un generico [T]:
class StandardResponse(BaseModel, Generic[T]):
    status: str = "success"  # Tiene un estado "success"
    message: str  # Tiene un mensaje.
    data: Optional[T] = None  # data es de tipo "T"
    # Es Optional por si un DELETE no devuelve datos.


"""

# Ejemplo: Devolver una lista de objetos
@router.get("/", response_model=StandardResponse[List[CategoriaRead]])
def list_categorias():
    lista_db = [] # Simulación DB
    
    return StandardResponse(
        status="success",
        message="Lista de categorías recuperada",
        data=lista_db
    )

"""
