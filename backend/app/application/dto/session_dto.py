from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class SessionCreateRequest(BaseModel):
    title: str | None = Field(default=None, max_length=120)


class SessionResponse(BaseModel):
    id: str
    title: str | None
    status: str
    created_at: datetime
    updated_at: datetime
    closed_at: datetime | None = None