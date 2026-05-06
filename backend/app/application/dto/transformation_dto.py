from __future__ import annotations

from pydantic import BaseModel, Field


class TransformVersionRequest(BaseModel):
    version_id: str = Field(min_length=1, max_length=100)
    transformation_type: str = Field(min_length=1, max_length=50)
    instruction: str | None = Field(default=None, max_length=500)
    language: str | None = Field(default="auto", max_length=10)