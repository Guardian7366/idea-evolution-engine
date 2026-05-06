from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ComparisonRequest(BaseModel):
    idea_id: str = Field(min_length=1, max_length=100)
    left_version_id: str = Field(min_length=1, max_length=100)
    right_version_id: str = Field(min_length=1, max_length=100)
    language: str | None = Field(default="auto", max_length=10)


class ComparisonResponse(BaseModel):
    id: str
    idea_id: str
    left_version_id: str
    right_version_id: str
    comparison_text: str | None
    created_at: datetime