from __future__ import annotations

from app.domain.entities.idea_version import IdeaVersion
from app.domain.value_objects.transformation_type import TransformationType
from app.domain.value_objects.version_status import VersionStatus


def map_transformation_payload_to_entity(
    payload: dict,
    *,
    idea_id: str,
    version_number: int,
    parent_version_id: str,
    transformation_type: TransformationType,
    user_instruction: str | None,
) -> IdeaVersion:
    return IdeaVersion(
        id=payload["id"],
        idea_id=idea_id,
        content=payload["content"],
        version_number=version_number,
        transformation_type=transformation_type,
        source_variant_id=None,
        parent_version_id=parent_version_id,
        user_instruction=user_instruction,
        is_active=True,
        status=VersionStatus.ACTIVE,
        created_at=payload["created_at"],
        updated_at=payload["updated_at"],
    )