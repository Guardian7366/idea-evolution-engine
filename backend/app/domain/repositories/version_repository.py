from abc import ABC, abstractmethod
from typing import List, Optional
from sqlite3 import Cursor

from app.domain.entities.idea_version import IdeaVersion
from app.domain.value_objects.version_status import VersionStatus


class VersionRepository(ABC):
    """
    Contrato abstracto para la persistencia de IdeaVersions.
    Cualquier implementación debe respetar exactamente estos métodos y firmas.
    """

    @abstractmethod
    async def save(self, version: IdeaVersion, cursor: Cursor) -> IdeaVersion:
        """
        Persiste una versión nueva o actualiza una existente.
        """
        ...

    @abstractmethod
    async def get_by_id(self, version_id: str, cursor: Cursor) -> Optional[IdeaVersion]:
        """Retorna una versión por su ID, o None si no existe."""
        ...

    @abstractmethod
    async def get_by_idea_id(self, idea_id: str, cursor: Cursor) -> List[IdeaVersion]:
        """
        Retorna todas las versiones de una idea ordenadas por version_number ASC.
        """
        ...

    @abstractmethod
    async def get_latest_by_idea_id(self, idea_id: str, cursor: Cursor) -> Optional[IdeaVersion]:
        """
        Retorna la versión con el version_number más alto para una idea.
        """
        ...

    @abstractmethod
    async def get_by_status(
        self, session_id: str, status: VersionStatus, cursor: Cursor
    ) -> List[IdeaVersion]:
        """
        Retorna versiones de una sesión filtradas por estado.
        """
        ...

    @abstractmethod
    async def get_next_version_number(self, idea_id: str, cursor: Cursor) -> int:
        """
        Calcula el próximo número de versión para una idea de forma segura.
        """
        ...

    @abstractmethod
    async def delete(self, version_id: str, cursor: Cursor) -> bool:
        """
        Elimina una versión por su ID. Retorna True si existía y fue eliminada, False si no existía.
        """
        ...
