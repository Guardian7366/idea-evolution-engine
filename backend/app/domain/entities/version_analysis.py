from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class VersionAnalysis:
    id: str
    version_id: str
    analysis_type: str
    content: str
    created_at: datetime