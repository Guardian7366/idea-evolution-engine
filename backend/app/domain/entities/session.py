from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.value_objects.session_status import SessionStatus


@dataclass
class Session:
    id: str
    title: str | None
    status: SessionStatus
    created_at: datetime
    updated_at: datetime
    closed_at: datetime | None = None