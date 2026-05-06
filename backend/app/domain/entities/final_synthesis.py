from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class FinalSynthesis:
    id: str
    idea_id: str
    version_id: str
    summary: str
    value_proposition: str
    target_audience: str
    structured_description: str
    next_steps: str
    created_at: datetime