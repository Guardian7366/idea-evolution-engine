from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class VersionResponse(BaseModel):
    id: str
    idea_id: str
    content: str
    version_number: int
    transformation_type: str
    source_variant_id: str | None = None
    parent_version_id: str | None = None
    user_instruction: str | None = None
    is_active: bool
    status: str
    created_at: datetime
    updated_at: datetime


class VersionListResponse(BaseModel):
    items: list[VersionResponse]