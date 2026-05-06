from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.value_objects.idea_content import IdeaContent


@dataclass
class Idea:
    id: str
    session_id: str
    content: IdeaContent
    created_at: datetime
    updated_at: datetime
    title: str | None = None