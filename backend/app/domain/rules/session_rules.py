from __future__ import annotations

from app.domain.entities.session import Session
from app.domain.value_objects.session_status import SessionStatus


def ensure_session_is_active(session: Session) -> None:
    if session.status != SessionStatus.ACTIVE:
        raise ValueError("Session must be active.")