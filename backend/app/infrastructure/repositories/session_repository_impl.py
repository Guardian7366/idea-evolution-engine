from __future__ import annotations

from datetime import datetime
from sqlalchemy.orm import Session as DBSession

from app.domain.entities.session import Session
from app.domain.repositories.session_repository import SessionRepository
from app.domain.value_objects.session_status import SessionStatus
from app.infrastructure.persistence.models.session_model import SessionModel


class SqliteSessionRepository(SessionRepository):
    def __init__(self, db: DBSession) -> None:
        self.db = db

    def save(self, session: Session) -> Session:
        model = SessionModel(
            id=session.id,
            title=session.title,
            status=session.status.value,
            created_at=session.created_at.isoformat(),
            updated_at=session.updated_at.isoformat(),
            closed_at=session.closed_at.isoformat() if session.closed_at else None,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return Session(
            id=model.id,
            title=model.title,
            status=SessionStatus(model.status),
            created_at=session.created_at,
            updated_at=session.updated_at,
            closed_at=session.closed_at,
        )

    def get_by_id(self, session_id: str) -> Session | None:
        model = (
            self.db.query(SessionModel)
            .filter(SessionModel.id == session_id)
            .first()
        )
        if model is None:
            return None

        return Session(
            id=model.id,
            title=model.title,
            status=SessionStatus(model.status),
            created_at=datetime.fromisoformat(model.created_at),
            updated_at=datetime.fromisoformat(model.updated_at),
            closed_at=datetime.fromisoformat(model.closed_at) if model.closed_at else None,
        )