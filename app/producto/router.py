from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.core.schema import StandardResponse
from . import schema, service

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=StandardResponse[List[schema.ProductoRead]])
def listar(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    productos = service.obtener_productos(session=session, skip=skip, limit=limit)
    return StandardResponse(message="Productos listados correctamente", data=productos)


@router.get("/{id}", response_model=StandardResponse[schema.ProductoRead])
def detalle(id: int, session: Session = Depends(get_session)):
    producto = service.obtener_producto_por_id(session=session, id=id)
    return StandardResponse(message="Producto obtenido correctamente", data=producto)


@router.post(
    "/",
    response_model=StandardResponse[schema.ProductoRead],
    status_code=status.HTTP_201_CREATED,
)
def crear(producto: schema.ProductoCreate, session: Session = Depends(get_session)):
    nuevo_producto = service.crear_producto(session=session, data=producto)
    return StandardResponse(message="Producto creado exitosamente", data=nuevo_producto)


@router.put("/{id}", response_model=StandardResponse[schema.ProductoRead])
def actualizar(
    id: int,
    producto: schema.ProductoUpdate,
    session: Session = Depends(get_session),
):
    producto_actualizado = service.actualizar_producto(
        session=session, id=id, data=producto
    )
    return StandardResponse(
        message="Producto actualizado exitosamente", data=producto_actualizado
    )


@router.delete("/{id}", response_model=StandardResponse[dict])
def eliminar(id: int, session: Session = Depends(get_session)):
    resultado = service.eliminar_producto(session=session, id=id)
    return StandardResponse(
        message=f"Producto {id} eliminado correctamente", data=resultado
    )
