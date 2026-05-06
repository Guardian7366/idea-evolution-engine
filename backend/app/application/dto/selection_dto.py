from __future__ import annotations

from pydantic import BaseModel, Field


class VariantSelectionRequest(BaseModel):
    idea_id: str = Field(min_length=1, max_length=100)
    variant_id: str = Field(min_length=1, max_length=100)
    language: str | None = Field(default="auto", max_length=10)