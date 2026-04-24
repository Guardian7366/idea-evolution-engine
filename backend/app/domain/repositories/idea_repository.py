from abc import ABC, abstractmethod
from typing import List, Optional
from sqlite3 import Cursor

from app.domain.entities.idea import Idea


class IdeaRepository(ABC):
    """
    Contrato abstracto para la persistencia de Ideas.
    Cualquier implementación (SQLite, mock en memoria, PostgreSQL, etc.)
    debe respetar exactamente estos métodos y tipos de retorno.
    """

    @abstractmethod
    async def save(self, idea: Idea, cursor: Cursor) -> Idea:
        """Persiste una idea nueva o actualiza una existente. Retorna la idea persistida."""
        ...

    @abstractmethod
    async def get_by_id(self, idea_id: str, cursor: Cursor) -> Optional[Idea]:
        """Retorna una idea por su ID, o None si no existe."""
        ...

    @abstractmethod
    async def get_by_session_id(self, session_id: str, cursor: Cursor) -> List[Idea]:
        """Retorna todas las ideas asociadas a una sesión, incluyendo archivadas."""
        ...

    @abstractmethod
    async def get_active_by_session_id(self, session_id: str, cursor: Cursor) -> List[Idea]:
        """
        Retorna solo las ideas no archivadas de una sesión (is_archived=False).
        """
        ...

    @abstractmethod
    async def delete(self, idea_id: str, cursor: Cursor) -> bool:
        """
        Elimina una idea por su ID. Retorna True si existía y fue eliminada, False si no existía.
        """
        ...

    @abstractmethod
    async def exists(self, idea_id: str, cursor: Cursor) -> bool:
        """
        Verifica si una idea existe sin cargarla completa. Más eficiente que get_by_id().
        """
        ...
