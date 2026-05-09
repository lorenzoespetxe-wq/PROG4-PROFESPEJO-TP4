from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.producto_categoria.model import ProductoCategoria


class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    # Asigna automaticamente fecha y hora en el momento de registro.
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    # Estos campos son opcionales, porque se usaran cuando se haga un PUT / PATCH.
    fecha_ultima_modificacion: Optional[datetime] = Field(default=None)
    usuario_ultima_modificacion: Optional[str] = Field(default=None)

    # Relación hacia la tabla intermedia
    producto_categorias: List["ProductoCategoria"] = Relationship(
        back_populates="categoria", cascade_delete=True
    )
