from __future__ import annotations

from app.domain.entities.version_analysis import VersionAnalysis


def map_analysis_payload_to_entity(payload: dict, version_id: str) -> VersionAnalysis:
    return VersionAnalysis(
        id=payload["id"],
        version_id=version_id,
        analysis_type=payload["analysis_type"],
        content=payload["content"],
        created_at=payload["created_at"],
    )