"""
session_repository.py — Contrato abstracto para la persistencia de Sessions.

CAMBIOS TAREA 5 (Alineación con persistencia real):

1. get_all() ahora acepta limit y offset además de status.
   La implementación real usa paginación (LIMIT ? OFFSET ?) en la query SQL.
   El contrato anterior solo tenía status=None, lo que hacía que la impl
   recibiera parámetros que el contrato no reconocía — contrato roto.

   Valores por defecto conservadores para no romper llamadas existentes:
   - limit=50: máximo razonable para no sobrecargar la UI.
   - offset=0: primera página por defecto.
   - status=None: sin filtro por estado por defecto.

2. delete() ahora retorna bool en lugar de None, igual que en IdeaRepository.
   La implementación ya retorna True/False y el contrato debe reflejarlo.

3. Se añadió get_by_status() que ya existe en la implementación pero faltaba
   en el contrato abstracto. Necesario para que los servicios puedan filtrar
   sesiones por estado de forma formal.
"""

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
    async def get_by_status(self, status: SessionStatus) -> List[Session]:
        """
        Retorna todas las sesiones con un estado específico sin paginación.

        Diferencia con get_all(status=X):
        - get_all() está pensado para el endpoint de listado con paginación.
        - Este método es para uso interno de servicios que necesitan
          todas las sesiones de un estado sin límite de páginas.
          Ejemplo: verificar cuántas sesiones están ACTIVE al arrancar.
        """
        ...

    @abstractmethod
    async def delete(self, session_id: str) -> bool:
        """
        Elimina una sesión por su ID.
        Retorna True si existía y fue eliminada, False si no existía.
        """
        ...