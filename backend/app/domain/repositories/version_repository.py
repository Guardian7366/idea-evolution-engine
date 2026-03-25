from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.idea_version import IdeaVersion
from app.domain.value_objects.version_status import VersionStatus


class VersionRepository(ABC):
    """
    Contrato abstracto para la persistencia de IdeaVersions.
    """

    @abstractmethod
    async def save(self, version: IdeaVersion) -> IdeaVersion:
        """Persiste una versión nueva o actualiza una existente."""
        ...

    @abstractmethod
    async def get_by_id(self, version_id: str) -> Optional[IdeaVersion]:
        """Retorna una versión por su ID, o None si no existe."""
        ...

    @abstractmethod
    async def get_by_idea_id(self, idea_id: str) -> List[IdeaVersion]:
        """
        Retorna todas las versiones de una idea, ordenadas por version_number ascendente.
        """
        ...

    @abstractmethod
    async def get_latest_by_idea_id(self, idea_id: str) -> Optional[IdeaVersion]:
        """
        Retorna la versión más reciente de una idea.
        Útil para continuar el flujo de evolución desde el último estado.
        """
        ...

    @abstractmethod
    async def get_by_status(self, session_id: str, status: VersionStatus) -> List[IdeaVersion]:
        """Retorna versiones de una sesión filtradas por estado."""
        ...

    @abstractmethod
    async def get_next_version_number(self, idea_id: str) -> int:
        """
        Calcula el próximo número de versión para una idea.
        Evita colisiones y garantiza secuencia continua.
        """
        ...

    @abstractmethod
    async def delete(self, version_id: str) -> bool:
        """Elimina una versión. Retorna True si existía y fue eliminada."""
        ...