from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.idea_version import IdeaVersion


class VersionRepository(ABC):
    @abstractmethod
    def save(self, version: IdeaVersion) -> IdeaVersion:
        raise NotImplementedError

    @abstractmethod
    def list_by_idea_id(self, idea_id: str) -> list[IdeaVersion]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, version_id: str) -> IdeaVersion | None:
        raise NotImplementedError

    @abstractmethod
    def get_active_by_idea_id(self, idea_id: str) -> IdeaVersion | None:
        raise NotImplementedError

    @abstractmethod
    def deactivate_active_versions(self, idea_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def activate_version(self, version_id: str) -> IdeaVersion | None:
        raise NotImplementedError