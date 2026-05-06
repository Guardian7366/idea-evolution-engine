from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class IdeaVariant:
    id: str
    idea_id: str
    title: str
    description: str
    order_index: int
    created_at: datetime
    is_selected: bool = False
    selected_at: datetime | None = None