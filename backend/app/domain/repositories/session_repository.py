from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.session import Session


class SessionRepository(ABC):
    @abstractmethod
    def save(self, session: Session) -> Session:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, session_id: str) -> Session | None:
        raise NotImplementedError