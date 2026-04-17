"""
variant_mapper.py — Maps raw Ollama JSON output to IdeaVariantItem DTOs.

Called by: ollama_provider.py → generate_variants
"""

import json
import uuid
from typing import Literal

from app.application.dto.variant_dto import IdeaVariantItem

_VALID_TYPES: set[str] = {"expansion", "focus", "creative_twist"}

_FALLBACK_VARIANTS: list[IdeaVariantItem] = [
    IdeaVariantItem(
        variant_id=str(uuid.uuid4()),
        title="Expanded Concept",
        content="A broader interpretation of the idea with wider scope and more potential.",
        variant_type="expansion",
    ),
    IdeaVariantItem(
        variant_id=str(uuid.uuid4()),
        title="Focused Direction",
        content="A sharper, more targeted version of the idea aimed at a specific use case.",
        variant_type="focus",
    ),
    IdeaVariantItem(
        variant_id=str(uuid.uuid4()),
        title="Creative Twist",
        content="An unconventional reframing of the idea that explores an unexpected angle.",
        variant_type="creative_twist",
    ),
]


def map_variants(raw_json: str) -> list[IdeaVariantItem]:
    """
    Parse Ollama's JSON response and return a list of IdeaVariantItem.

    Falls back to generic variants if the response is malformed or missing keys.
    """
    try:
        data = json.loads(raw_json)
        raw_variants = data.get("variants", [])
        if not isinstance(raw_variants, list) or len(raw_variants) == 0:
            return _FALLBACK_VARIANTS

        result: list[IdeaVariantItem] = []
        for item in raw_variants:
            variant_type = item.get("variant_type", "")
            if variant_type not in _VALID_TYPES:
                variant_type = "expansion"

            result.append(
                IdeaVariantItem(
                    variant_id=str(uuid.uuid4()),
                    title=str(item.get("title", "Variant")).strip()[:60] or "Variant",
                    content=str(item.get("content", "")).strip() or "No content provided.",
                    variant_type=variant_type,  # type: ignore[arg-type]
                )
            )

        # Garantiza exactamente 3 variantes combinando IA + fallback
        if len(result) >= 3:
            return result[:3]

        # Si faltan variantes, completar con fallback sin perder las reales
        needed = 3 - len(result)
        fallback_extra = _FALLBACK_VARIANTS[:needed]

        return result + fallback_extra

    except (json.JSONDecodeError, AttributeError, TypeError):
        return _FALLBACK_VARIANTS
