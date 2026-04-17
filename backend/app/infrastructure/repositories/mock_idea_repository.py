"""
mock_idea_repository.py — Implementación en memoria de IdeaRepository.

Este mock existe para que VersionService pueda verificar que una idea
existe antes de crearle versiones, sin depender de la BD real.

Cuando idea_service.py esté implementado completamente y tenga su propio
repositorio persistente, este mock se reemplaza en deps.py.
"""

from typing import Dict, List, Optional

from app.domain.entities.idea import Idea
from app.domain.repositories.idea_repository import IdeaRepository


class MockIdeaRepository(IdeaRepository):
    """
    Repositorio de ideas en memoria.
    Mismo patrón que MockSessionRepository y MockVersionRepository.
    """

    def __init__(self) -> None:
        self._store: Dict[str, Idea] = {}

    async def save(self, idea: Idea) -> Idea:
        self._store[idea.id] = idea
        return idea

    async def get_by_id(self, idea_id: str) -> Optional[Idea]:
        return self._store.get(idea_id)

    async def get_by_session_id(self, session_id: str) -> List[Idea]:
        return [i for i in self._store.values() if i.session_id == session_id]

    async def get_active_by_session_id(self, session_id: str) -> List[Idea]:
        """
        Retorna las ideas activas de una sesión.

        IMPORTANTE:
        En el modelo actual de Idea no existe is_active.
        La idea se considera "activa" mientras NO esté archivada.
        """
        return [
            i for i in self._store.values()
            if i.session_id == session_id and not i.is_archived
        ]

    async def delete(self, idea_id: str) -> bool:
        if idea_id in self._store:
            del self._store[idea_id]
            return True
        return False

    async def exists(self, idea_id: str) -> bool:
        return idea_id in self._store