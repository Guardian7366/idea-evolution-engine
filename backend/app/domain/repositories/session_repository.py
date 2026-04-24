from abc import ABC, abstractmethod
from typing import List, Optional
from sqlite3 import Cursor

from app.domain.entities.session import Session
from app.domain.value_objects.session_status import SessionStatus


class SessionRepository(ABC):
    """
    Contrato abstracto para la persistencia de Sessions.
    Cualquier implementación debe respetar exactamente estos métodos y firmas.
    """

    @abstractmethod
    async def save(self, session: Session, cursor: Cursor) -> Session:
        """Persiste una sesión nueva o actualiza una existente."""
        ...

    @abstractmethod
    async def get_by_id(self, session_id: str, cursor: Cursor) -> Optional[Session]:
        """Retorna una sesión por su ID, o None si no existe."""
        ...

    @abstractmethod
    async def get_all(
        self,
        status: Optional[SessionStatus] = None,
        limit: int = 50,
        offset: int = 0,
        cursor: Cursor = None
    ) -> List[Session]:
        """
        Retorna sesiones paginadas, opcionalmente filtradas por estado.
        """
        ...

    @abstractmethod
    async def delete(self, session_id: str, cursor: Cursor) -> bool:
        """
        Elimina una sesión por su ID. Retorna True si existía y fue eliminada, False si no existía.
        """
        ...
    @abstractmethod
    async def exists(self, session_id: str, cursor: Cursor) -> bool:
        """
        Verifica si una sesión existe sin cargarla completa.
        """
        ...
