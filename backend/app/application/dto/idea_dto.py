from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class IdeaCreateRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=2000)
    title: str | None = Field(default=None, max_length=120)


class IdeaResponse(BaseModel):
    id: str
    session_id: str
    content: str
    title: str | None
    created_at: datetime
    updated_at: datetime