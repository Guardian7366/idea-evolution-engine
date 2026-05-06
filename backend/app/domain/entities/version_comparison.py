from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class VersionComparison:
    id: str
    idea_id: str
    left_version_id: str
    right_version_id: str
    created_at: datetime
    comparison_text: str | None = None