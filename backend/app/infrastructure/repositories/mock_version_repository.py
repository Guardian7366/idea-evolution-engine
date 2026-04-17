"""
mock_version_repository.py — Implementación en memoria de VersionRepository.

Mismo patrón que MockSessionRepository: datos en memoria, se pierden al reiniciar.
Reemplazar por VersionRepositoryImpl(db) en deps.py cuando la BD esté lista.
"""

from typing import Dict, List, Optional

from app.domain.entities.idea_version import IdeaVersion
from app.domain.repositories.version_repository import VersionRepository
from app.domain.value_objects.version_status import VersionStatus


class MockVersionRepository(VersionRepository):
    """
    Repositorio de versiones en memoria.
    El dict _store usa version.id como clave.
    """

    def __init__(self) -> None:
        self._store: Dict[str, IdeaVersion] = {}

    async def save(self, version: IdeaVersion) -> IdeaVersion:
        self._store[version.id] = version
        return version

    async def get_by_id(self, version_id: str) -> Optional[IdeaVersion]:
        return self._store.get(version_id)

    async def get_by_idea_id(self, idea_id: str) -> List[IdeaVersion]:
        """
        Retorna todas las versiones de una idea ordenadas por version_number ascendente.
        En la implementación real sería un ORDER BY version_number ASC.
        """
        versions = [v for v in self._store.values() if v.idea_id == idea_id]
        return sorted(versions, key=lambda v: v.version_number)

    async def get_latest_by_idea_id(self, idea_id: str) -> Optional[IdeaVersion]:
        """
        Retorna la versión con el version_number más alto para una idea.
        Retorna None si la idea no tiene versiones todavía.
        """
        versions = await self.get_by_idea_id(idea_id)
        return versions[-1] if versions else None

    async def get_by_status(self, session_id: str, status: VersionStatus) -> List[IdeaVersion]:
        """
        ⚠️ IMPORTANTE:
        Este método NO es compatible con el modelo actual.

        IdeaVersion NO tiene session_id, solo idea_id.
        Para poder filtrar por sesión, se necesitaría:
        1. Acceso a IdeaRepository para mapear idea_id → session_id
        2. O agregar session_id a IdeaVersion (decisión de dominio)

        Por ahora este método se deshabilita explícitamente para evitar errores silenciosos.
        """

        raise NotImplementedError(
            "get_by_status no está soportado con el modelo actual de IdeaVersion. "
            "Debe rediseñarse junto con persistencia real en Semana 2."
        )
            

    async def get_next_version_number(self, idea_id: str) -> int:
        """
        Calcula el próximo número de versión para una idea.
        Si no hay versiones previas, retorna 1.
        Si hay 3 versiones (1, 2, 3), retorna 4.

        En la implementación real con BD sería:
            SELECT COALESCE(MAX(version_number), 0) + 1
            FROM idea_versions WHERE idea_id = :idea_id
        """
        versions = await self.get_by_idea_id(idea_id)
        if not versions:
            return 1
        return max(v.version_number for v in versions) + 1

    async def delete(self, version_id: str) -> bool:
        if version_id in self._store:
            del self._store[version_id]
            return True
        return False