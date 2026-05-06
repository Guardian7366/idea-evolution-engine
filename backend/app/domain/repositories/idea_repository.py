from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.idea import Idea
from app.domain.entities.idea_variant import IdeaVariant


class IdeaRepository(ABC):
    @abstractmethod
    def save_idea(self, idea: Idea) -> Idea:
        raise NotImplementedError

    @abstractmethod
    def get_idea_by_id(self, idea_id: str) -> Idea | None:
        raise NotImplementedError

    @abstractmethod
    def save_variants(self, variants: list[IdeaVariant]) -> list[IdeaVariant]:
        raise NotImplementedError

    @abstractmethod
    def list_variants_by_idea_id(self, idea_id: str) -> list[IdeaVariant]:
        raise NotImplementedError

    @abstractmethod
    def get_variant_by_id(self, variant_id: str) -> IdeaVariant | None:
        raise NotImplementedError

    @abstractmethod
    def mark_variant_selected(self, variant_id: str) -> IdeaVariant | None:
        raise NotImplementedError