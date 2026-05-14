"""
Implementamos el patrón de "Repositorio Base", con el objetivo de definir
las operaciones comunes del CRUD en una clase genérica, y no reescribir
el mismo código para cada modelo.
"""

# Importamos herramientas de tipado:
from typing import Generic, TypeVar, Type, Sequence

# Importamos el gestor de transacciones, SQLModel (clase base ORM)
# y el constructor de consultas (select):
from sqlmodel import Session, SQLModel, select

# Creamos un genérico que abarque todos los modelos que hemos definido:
ModelT = TypeVar("ModelT", bound=SQLModel)


# Definimos la clase genérica, que los repositorios de los módulos
# van a heredar. Cuándo los hagan, el genérico se convertira en el
# modelo de esa entidad:
class BaseRepository(Generic[ModelT]):
    # Constructor: requiere la sesión de la DB y la clase del modelo:
    def __init__(self, session: Session, model: Type[ModelT]) -> None:
        self.session = session  # almacena la sesión y el modelo
        self.model = model  # como atributos.

    # GET by ID:
    # Se recibe a si mismo (sesión + modelo) y al id a buscar:
    def get_by_id(self, id: int) -> ModelT | None:
        return self.session.get(self.model, id)
        # Devuelve la instancia del modelo con el id proporcionado.

    # GET ALL:
    # Se recibe a si mismo, tiene paginación incorporada:
    def get_all(self, offset: int = 0, limit: int = 20) -> Sequence[ModelT]:
        return self.session.exec(select(self.model).offset(offset).limit(limit)).all()
        # al devolver, salta offset(0) registros y trae hasta limit(20).

    # ADD:
    # Se recibe a si mismo y a una instancia de el modelo en cuestión.
    def add(self, instance: ModelT) -> ModelT:

        # Colocamos el objeto en estado pendiente:
        self.session.add(instance)

        # Se envía la sentancia INSERT a la DB, pero aún no hace el commit,
        # la DB aprovecha par validar la operación y asignar IDs:
        self.session.flush()

        # Refresca y sincroniza el objeto Python ocn la DB, capturando
        # los datos autogenerados como el id o timestamps:
        self.session.refresh(instance)

        return instance  # Devuelve el objeto actualizado.

    # DELETE:
    # Se recibe a si mismo, y nuevamente a una instancia de el modelo:
    def delete(self, instance: ModelT) -> None:
        self.session.delete(instance)  # marcar el objeto a eliminar.

        # Envía la sentencia, pero nuevamente el commit esta a cargo del UoW:
        self.session.flush()
