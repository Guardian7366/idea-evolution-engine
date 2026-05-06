from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class SynthesisRequest(BaseModel):
    idea_id: str = Field(min_length=1, max_length=100)
    version_id: str = Field(min_length=1, max_length=100)
    language: str | None = Field(default="auto", max_length=10)


class SynthesisResponse(BaseModel):
    id: str
    idea_id: str
    version_id: str
    summary: str
    value_proposition: str
    target_audience: str
    structured_description: str
    next_steps: str
    created_at: datetime