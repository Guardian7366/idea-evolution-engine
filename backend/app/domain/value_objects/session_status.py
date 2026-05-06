from __future__ import annotations

from enum import Enum


class SessionStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"