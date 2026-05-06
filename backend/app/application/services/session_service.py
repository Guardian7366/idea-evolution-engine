from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.application.dto.session_dto import SessionCreateRequest, SessionResponse
from app.domain.entities.session import Session
from app.domain.repositories.session_repository import SessionRepository
from app.domain.value_objects.session_status import SessionStatus


class SessionService:
    def __init__(self, repository: SessionRepository) -> None:
        self.repository = repository

    def create_session(self, data: SessionCreateRequest) -> SessionResponse:
        now = datetime.now(timezone.utc)
        session = Session(
            id=f"ses_{uuid4().hex}",
            title=data.title,
            status=SessionStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )
        saved = self.repository.save(session)
        return self._to_response(saved)

    def get_session_by_id(self, session_id: str) -> SessionResponse | None:
        session = self.repository.get_by_id(session_id)
        if session is None:
            return None
        return self._to_response(session)

    def _to_response(self, session: Session) -> SessionResponse:
        return SessionResponse(
            id=session.id,
            title=session.title,
            status=session.status.value,
            created_at=session.created_at,
            updated_at=session.updated_at,
            closed_at=session.closed_at,
        )