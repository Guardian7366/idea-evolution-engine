from __future__ import annotations

from app.domain.entities.version_comparison import VersionComparison


def map_comparison_payload_to_entity(
    payload: dict,
    *,
    idea_id: str,
    left_version_id: str,
    right_version_id: str,
) -> VersionComparison:
    return VersionComparison(
        id=payload["id"],
        idea_id=idea_id,
        left_version_id=left_version_id,
        right_version_id=right_version_id,
        comparison_text=payload["comparison_text"],
        created_at=payload["created_at"],
    )