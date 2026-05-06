from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class PerspectiveRequest(BaseModel):
    version_id: str = Field(min_length=1, max_length=100)
    perspective: str = Field(min_length=1, max_length=500)
    language: str | None = Field(default="auto", max_length=10)


class PerspectiveResponse(BaseModel):
    id: str
    version_id: str
    analysis_type: str
    content: str
    created_at: datetime