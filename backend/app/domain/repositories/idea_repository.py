from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.idea import Idea


class IdeaRepository(ABC):
    """
    Contrato abstracto para la persistencia de Ideas.
    La capa de dominio depende de esta interfaz, nunca de la implementación concreta.
    La implementación real vive en infrastructure/repositories/idea_repository_impl.py
    """

    @abstractmethod
    async def save(self, idea: Idea) -> Idea:
        """Persiste una idea nueva o actualiza una existente."""
        ...

    @abstractmethod
    async def get_by_id(self, idea_id: str) -> Optional[Idea]:
        """Retorna una idea por su ID, o None si no existe."""
        ...

    @abstractmethod
    async def get_by_session_id(self, session_id: str) -> list[Idea]:
        """Retorna todas las ideas asociadas a una sesión."""
        ...

    @abstractmethod
    async def delete(self, idea_id: str) -> None:
        """Elimina una idea por su ID."""
        ...