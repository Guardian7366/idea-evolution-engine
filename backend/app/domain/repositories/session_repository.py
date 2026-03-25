from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.session import Session
from app.domain.value_objects.session_status import SessionStatus


class SessionRepository(ABC):
    """
    Contrato abstracto para la persistencia de Sessions.
    """

    @abstractmethod
    async def save(self, session: Session) -> Session:
        """Persiste una sesión nueva o actualiza una existente."""
        ...

    @abstractmethod
    async def get_by_id(self, session_id: str) -> Optional[Session]:
        """Retorna una sesión por su ID, o None si no existe."""
        ...

    @abstractmethod
    async def get_all(self, status: Optional[SessionStatus] = None) -> list[Session]:
        """
        Retorna todas las sesiones.
        Si se provee un status, filtra por él.
        """
        ...

    @abstractmethod
    async def delete(self, session_id: str) -> None:
        """Elimina una sesión por su ID."""
        ...