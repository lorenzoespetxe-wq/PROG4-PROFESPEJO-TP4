from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.core.schema import StandardResponse
from . import schema, service

router = APIRouter(prefix="/producto-categorias", tags=["ProductoCategorías"])


@router.get("/", response_model=StandardResponse[List[schema.ProductoCategoriaRead]])
def listar(session: Session = Depends(get_session)):
    relaciones = service.obtener_relaciones(session=session)
    return StandardResponse(
        message="Relaciones listadas correctamente", data=relaciones
    )


@router.get(
    "/producto/{producto_id}",
    response_model=StandardResponse[List[schema.ProductoCategoriaRead]],
)
def listar_por_producto(producto_id: int, session: Session = Depends(get_session)):
    relaciones = service.obtener_categorias_de_producto(
        session=session, producto_id=producto_id
    )
    return StandardResponse(
        message=f"Categorías del producto {producto_id} obtenidas", data=relaciones
    )
