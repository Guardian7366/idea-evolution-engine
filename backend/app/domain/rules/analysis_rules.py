from __future__ import annotations

from app.domain.entities.version_comparison import VersionComparison


def ensure_comparison_versions_are_distinct(comparison: VersionComparison) -> None:
    if comparison.left_version_id == comparison.right_version_id:
        raise ValueError("Compared versions must be different.")