"""
Implementamos el patrón "Unit of Work", para gestionar que las
transacciones de la DB sean seguras, y se implementen atomicamente,
o no se implemten "at all".

Si el conjunto de operaciones si implementa sin errores, se hace un
commit, en caso contrario, si una o más fallan, se hace un rollback.

Complementa el Repositorio, ya que en nuestra arquitectura, el mismo
encola las consultas con flush pero no confirma las transacciones.
"""

# Importamos el gestor de sesiones de SQLModel:
from sqlmodel import Session


# Definimos la clase:
class UnitOfWork:
    # Constructor: recibe una sesión activa en la DB.
    def __init__(self, session: Session) -> None:
        self._session = session

    # Se ejecutará cuando entremos a los bloques with en los service:
    def __enter__(self) -> "UnitOfWork":
        return self  # Se devuelve a si misma para ser utilizada en el bloque.

    # Se ejecutará al salir del bloque with, ya sea naturalmente o por error:
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:  # si no hubo excepción...
            self._session.commit()  # ... haremos el commit.
        else:  # en el caso de que hubiera exepción...
            self._session.rollback()  # ... haremos el rollback.
        self._session.close()  # siempre cierra la sesión y libera recursos.

    # Para forzar una confirmación manual en algún caso:
    def commit(self) -> None:
        self._session.commit()

    # Para forzar un rollback en algún caso:
    def rollback(self) -> None:
        self._session.rollback()
