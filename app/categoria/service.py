from sqlmodel import Session, select, delete
from fastapi import HTTPException, status
from typing import List

from .model import Categoria
from .schema import CategoriaCreate, CategoriaUpdate
from app.producto_categoria.model import ProductoCategoria

from datetime import datetime


def crear_categoria(session: Session, data: CategoriaCreate) -> Categoria:
    # Validamos que no exista una categoría con el mismo nombre:
    statement = select(Categoria).where(Categoria.nombre == data.nombre)
    categoria_existente = session.exec(statement).first()

    if categoria_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una categoría con el nombre '{data.nombre}'",
        )

    # Creamos:
    db_categoria = Categoria.model_validate(data)
    session.add(db_categoria)
    session.commit()
    session.refresh(db_categoria)
    return db_categoria


def obtener_categorias(session: Session) -> List[Categoria]:
    return session.exec(select(Categoria)).all()


def obtener_categoria_por_id(session: Session, id: int) -> Categoria:
    categoria = session.get(Categoria, id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada",
        )
    return categoria


def actualizar_categoria(session: Session, id: int, data: CategoriaUpdate) -> Categoria:
    categoria_db = obtener_categoria_por_id(session, id)

    categoria_data = data.model_dump(exclude_unset=True)
    for key, value in categoria_data.items():
        setattr(categoria_db, key, value)

    # Inyectamos campos de auditoría:
    categoria_db.fecha_ultima_modificacion = datetime.utcnow()
    # Cuando implementemos JWT, aquí extraeríamos el usuario del token.
    # Por ahora, usamos un valor por defecto.
    categoria_db.usuario_ultima_modificacion = "sistema"

    session.add(categoria_db)
    session.commit()
    session.refresh(categoria_db)
    return categoria_db


def eliminar_categoria(session: Session, id: int) -> dict:
    categoria_db = obtener_categoria_por_id(session, id)
    session.delete(categoria_db)
    session.commit()
    return {"ok": True, "mensaje": f"Categoría {id} eliminada"}
