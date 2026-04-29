import uuid
from typing import Literal

from backend.app.application.dto.variant_dto import IdeaVariantItem
from backend.app.infrastructure.ai.mappers.base import LLMParseError, extract_json, require_keys

_VALID_TYPES = {"expansion", "focus", "creative_twist"}
_TYPE_FALLBACKS: dict[int, Literal["expansion", "focus", "creative_twist"]] = {
    0: "expansion",
    1: "focus",
    2: "creative_twist",
}


def map_variants_response(raw: str) -> list[IdeaVariantItem]:
    data = extract_json(raw)
    require_keys(data, ["variants"], "variants")

    raw_variants = data["variants"]
    if not isinstance(raw_variants, list) or len(raw_variants) == 0:
        raise LLMParseError(
            f"'variants' must be a non-empty list. Got: {type(raw_variants)}"
        )

    items: list[IdeaVariantItem] = []
    for i, v in enumerate(raw_variants[:3]):
        if not isinstance(v, dict):
            raise LLMParseError(f"Variant at index {i} is not a dict: {v!r}")

        title = str(v.get("title", "")).strip() or f"Variant {i + 1}"
        content = str(v.get("content", "")).strip()
        if not content:
            raise LLMParseError(f"Variant at index {i} has empty content.")

        raw_type = str(v.get("variant_type", "")).strip()
        variant_type = raw_type if raw_type in _VALID_TYPES else _TYPE_FALLBACKS[i]

        items.append(
            IdeaVariantItem(
                variant_id=f"variant_{uuid.uuid4().hex[:12]}",
                title=title,
                content=content,
                variant_type=variant_type,  # type: ignore[arg-type]
            )
        )

    # Pad with error if fewer than 3 returned
    if len(items) < 3:
        raise LLMParseError(
            f"Expected 3 variants, got {len(items)}. "
            "The model may not have followed the output format."
        )

    return items
