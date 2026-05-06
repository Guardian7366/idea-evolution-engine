from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class VariantResponse(BaseModel):
    id: str
    idea_id: str
    title: str
    description: str
    order_index: int
    is_selected: bool
    selected_at: datetime | None = None
    created_at: datetime


class VariantListResponse(BaseModel):
    items: list[VariantResponse]