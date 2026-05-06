from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.value_objects.transformation_type import TransformationType
from app.domain.value_objects.version_status import VersionStatus


@dataclass
class IdeaVersion:
    id: str
    idea_id: str
    content: str
    version_number: int
    transformation_type: TransformationType
    created_at: datetime
    updated_at: datetime
    source_variant_id: str | None = None
    parent_version_id: str | None = None
    user_instruction: str | None = None
    is_active: bool = False
    status: VersionStatus = VersionStatus.DERIVED