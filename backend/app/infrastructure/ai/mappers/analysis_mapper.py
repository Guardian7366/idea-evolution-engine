"""
analysis_mapper.py — Maps raw Ollama JSON output to comparison and perspective DTOs.

Called by: ollama_provider.py → compare_versions, explore_perspective
"""

import logging

from app.application.dto.comparison_dto import VersionComparisonResult
from app.application.dto.perspective_dto import PerspectiveAnalysisResult
from app.infrastructure.ai.mappers.base import LLMParseError, coerce_str_list, extract_json

logger = logging.getLogger(__name__)


def map_comparison(raw_json: str) -> VersionComparisonResult:
    """
    Parse Ollama's JSON and return a VersionComparisonResult.
    Falls back to a generic result on parse failure, with a warning log.
    """
    try:
        data = extract_json(raw_json)

        summary = str(data.get("summary", "")).strip()
        strengths_a = coerce_str_list(data.get("strengths_version_a"))
        strengths_b = coerce_str_list(data.get("strengths_version_b"))
        differences = coerce_str_list(data.get("key_differences"))
        recommendation = str(data.get("recommendation", "")).strip()

        if summary and strengths_a and strengths_b and differences and recommendation:
            return VersionComparisonResult(
                summary=summary,
                strengths_version_a=strengths_a,
                strengths_version_b=strengths_b,
                key_differences=differences,
                recommendation=recommendation,
            )

        logger.warning(
            "[analysis_mapper] map_comparison: respuesta incompleta — campos vacíos. "
            "summary=%s  str_a=%d  str_b=%d  diff=%d  rec=%s",
            bool(summary), len(strengths_a), len(strengths_b), len(differences), bool(recommendation),
        )

    except (LLMParseError, AttributeError, TypeError) as exc:
        logger.warning("[analysis_mapper] map_comparison: no se pudo parsear — %s", exc)

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
    Falls back to a generic result on parse failure, with a warning log.
    """
    try:
        data = extract_json(raw_json)

        summary = str(data.get("summary", "")).strip()
        observations = coerce_str_list(data.get("observations"))
        suggestion = str(data.get("suggestion", "")).strip()

        if summary and observations and suggestion:
            return PerspectiveAnalysisResult(
                perspective_type=perspective_type,
                summary=summary,
                observations=observations,
                suggestion=suggestion,
            )

        logger.warning(
            "[analysis_mapper] map_perspective (%s): respuesta incompleta — "
            "summary=%s  obs=%d  suggestion=%s",
            perspective_type, bool(summary), len(observations), bool(suggestion),
        )

    except (LLMParseError, AttributeError, TypeError) as exc:
        logger.warning("[analysis_mapper] map_perspective (%s): no se pudo parsear — %s",
                       perspective_type, exc)

    return PerspectiveAnalysisResult(
        perspective_type=perspective_type,
        summary=f"Analysis from the {perspective_type} perspective could not be completed.",
        observations=["The idea shows potential in this area", "Further refinement is recommended"],
        suggestion="Continue iterating and re-run this analysis after the next refinement.",
    )
