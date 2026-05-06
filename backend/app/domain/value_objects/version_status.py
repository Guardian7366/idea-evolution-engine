from __future__ import annotations

from enum import Enum


class VersionStatus(str, Enum):
    ACTIVE = "active"
    DERIVED = "derived"
    FINALIZED = "finalized"
    BASE = "base"