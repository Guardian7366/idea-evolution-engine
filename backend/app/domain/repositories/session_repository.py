from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.session import Session
from app.domain.value_objects.session_status import SessionStatus


class SessionRepository(ABC):
    """
    Contrato abstracto para la persistencia de Sessions.
    Cualquier implementación debe respetar exactamente estos métodos y firmas.
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
    async def get_all(
        self,
        status: Optional[SessionStatus] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Session]:
        """
        Retorna sesiones paginadas, opcionalmente filtradas por estado.

        Parámetros:
        - status: si se provee, retorna solo sesiones con ese estado.
        - limit: máximo de resultados por página. Default 50.
        - offset: desde qué posición empezar. Default 0 (primera página).

        La implementación SQLite ordena por created_at DESC (más recientes primero).

        NOTA PARA BACKEND 1: la implementación actual recibe limit y offset
        como parámetros posicionales. Alinear con esta firma donde status
        va primero y limit/offset tienen defaults.
        """
        ...

    @abstractmethod
    async def delete(self, session_id: str) -> bool:
        """
        Elimina una sesión por su ID.
        Retorna True si existía y fue eliminada, False si no existía.
        """
        ...
