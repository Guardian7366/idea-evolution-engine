"""
analysis_mapper.py — Maps raw Ollama JSON output to comparison and perspective DTOs.

Called by: ollama_provider.py → compare_versions, explore_perspective
"""

import json

from app.application.dto.comparison_dto import VersionComparisonResult
from app.application.dto.perspective_dto import PerspectiveAnalysisResult


def map_comparison(raw_json: str) -> VersionComparisonResult:
    """
    Parse Ollama's JSON and return a VersionComparisonResult.
    Falls back to a generic result on parse failure.
    """
    try:
        data = json.loads(raw_json)

        summary = str(data.get("summary", "")).strip()
        strengths_a = _coerce_list(data.get("strengths_version_a"))
        strengths_b = _coerce_list(data.get("strengths_version_b"))
        differences = _coerce_list(data.get("key_differences"))
        recommendation = str(data.get("recommendation", "")).strip()

        if summary and strengths_a and strengths_b and differences and recommendation:
            return VersionComparisonResult(
                summary=summary,
                strengths_version_a=strengths_a,
                strengths_version_b=strengths_b,
                key_differences=differences,
                recommendation=recommendation,
            )

    except (json.JSONDecodeError, AttributeError, TypeError):
        pass

    return VersionComparisonResult(
        summary="Both versions represent different stages of the idea's evolution.",
        strengths_version_a=["More aligned with the original concept", "Simpler and more direct"],
        strengths_version_b=["More processed and refined", "Clearer execution path"],
        key_differences=["Version A is closer to the original", "Version B shows more iteration"],
        recommendation="Continue with Version B as the working direction while keeping Version A as a reference.",
    )


def map_perspective(raw_json: str, perspective_type: str) -> PerspectiveAnalysisResult:
    """
    Parse Ollama's JSON and return a PerspectiveAnalysisResult.
    Falls back to a generic result on parse failure.
    """
    try:
        data = json.loads(raw_json)

        summary = str(data.get("summary", "")).strip()
        observations = _coerce_list(data.get("observations"))
        suggestion = str(data.get("suggestion", "")).strip()

        if summary and observations and suggestion:
            return PerspectiveAnalysisResult(
                perspective_type=perspective_type,
                summary=summary,
                observations=observations,
                suggestion=suggestion,
            )

    except (json.JSONDecodeError, AttributeError, TypeError):
        pass

    return PerspectiveAnalysisResult(
        perspective_type=perspective_type,
        summary=f"Analysis from the {perspective_type} perspective could not be completed.",
        observations=["The idea shows potential in this area", "Further refinement is recommended"],
        suggestion="Continue iterating and re-run this analysis after the next refinement.",
    )


def _coerce_list(value: object) -> list[str]:
    """Return a non-empty list of strings, or empty list if input is invalid."""
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []
