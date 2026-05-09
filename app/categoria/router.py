from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.core.schema import StandardResponse
from . import schema, service

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.get("/", response_model=StandardResponse[List[schema.CategoriaRead]])
def listar(session: Session = Depends(get_session)):
    categorias = service.obtener_categorias(session=session)
    return StandardResponse(
        message="Categorías listadas correctamente", data=categorias
    )


@router.get("/{id}", response_model=StandardResponse[schema.CategoriaRead])
def detalle(id: int, session: Session = Depends(get_session)):
    categoria = service.obtener_categoria_por_id(session=session, id=id)
    return StandardResponse(message="Categoría obtenida correctamente", data=categoria)


@router.post(
    "/",
    response_model=StandardResponse[schema.CategoriaRead],
    status_code=status.HTTP_201_CREATED,
)
def crear(categoria: schema.CategoriaCreate, session: Session = Depends(get_session)):
    nueva_categoria = service.crear_categoria(session=session, data=categoria)
    return StandardResponse(
        message="Categoría creada exitosamente", data=nueva_categoria
    )


@router.put("/{id}", response_model=StandardResponse[schema.CategoriaRead])
def actualizar(
    id: int,
    categoria: schema.CategoriaUpdate,
    session: Session = Depends(get_session),
):
    categoria_actualizada = service.actualizar_categoria(
        session=session, id=id, data=categoria
    )
    return StandardResponse(
        message="Categoría actualizada exitosamente", data=categoria_actualizada
    )


@router.delete("/{id}", response_model=StandardResponse[dict])
def eliminar(id: int, session: Session = Depends(get_session)):
    resultado = service.eliminar_categoria(session=session, id=id)
    return StandardResponse(
        message=f"Categoría {id} eliminada correctamente", data=resultado
    )
