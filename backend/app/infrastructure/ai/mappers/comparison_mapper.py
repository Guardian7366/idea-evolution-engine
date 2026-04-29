from backend.app.application.dto.comparison_dto import VersionComparisonResult
from backend.app.infrastructure.ai.mappers.base import LLMParseError, extract_json, require_keys

_REQUIRED_KEYS = [
    "summary",
    "strengths_version_a",
    "strengths_version_b",
    "key_differences",
    "recommendation",
]


def map_comparison_response(raw: str) -> VersionComparisonResult:
    data = extract_json(raw)
    require_keys(data, _REQUIRED_KEYS, "comparison")

    summary = str(data["summary"]).strip()
    recommendation = str(data["recommendation"]).strip()

    if not summary:
        raise LLMParseError("Comparison response has empty 'summary'.")
    if not recommendation:
        raise LLMParseError("Comparison response has empty 'recommendation'.")

    def parse_list(key: str) -> list[str]:
        raw_list = data[key]
        if not isinstance(raw_list, list):
            raise LLMParseError(f"'{key}' must be a list. Got: {type(raw_list)}")
        items = [str(item).strip() for item in raw_list if str(item).strip()]
        if not items:
            raise LLMParseError(f"'{key}' list is empty after filtering blank entries.")
        return items

    return VersionComparisonResult(
        summary=summary,
        strengths_version_a=parse_list("strengths_version_a"),
        strengths_version_b=parse_list("strengths_version_b"),
        key_differences=parse_list("key_differences"),
        recommendation=recommendation,
    )
