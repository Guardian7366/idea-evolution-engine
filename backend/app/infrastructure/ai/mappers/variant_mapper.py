"""
variant_mapper.py — Maps raw Ollama JSON output to IdeaVariantItem DTOs.

Called by: ollama_provider.py → generate_variants
"""

import logging
import uuid

from app.application.dto.variant_dto import IdeaVariantItem
from app.infrastructure.ai.mappers.base import LLMParseError, coerce_str_list, extract_json

logger = logging.getLogger(__name__)

_VALID_TYPES: set[str] = {"expansion", "focus", "creative_twist"}

# Fallback template — titles/contents are fixed, but IDs are always
# generated fresh at call time so two fallback requests never share IDs.
_FALLBACK_TEMPLATES = [
    ("Expanded Concept",
     "A broader interpretation of the idea with wider scope and more potential.",
     "expansion"),
    ("Focused Direction",
     "A sharper, more targeted version of the idea aimed at a specific use case.",
     "focus"),
    ("Creative Twist",
     "An unconventional reframing of the idea that explores an unexpected angle.",
     "creative_twist"),
]


def _make_fallback_variants() -> list[IdeaVariantItem]:
    """Return fallback variants with fresh UUIDs on every call."""
    return [
        IdeaVariantItem(
            variant_id=str(uuid.uuid4()),
            title=title,
            content=content,
            variant_type=vtype,  # type: ignore[arg-type]
        )
        for title, content, vtype in _FALLBACK_TEMPLATES
    ]


def map_variants(raw_json: str) -> list[IdeaVariantItem]:
    """
    Parse Ollama's JSON response and return exactly 3 IdeaVariantItem objects.

    Falls back to generic variants with fresh UUIDs if the response is malformed
    or missing keys. Pads with fallback items if fewer than 3 variants returned.
    """
    try:
        data = extract_json(raw_json)
        raw_variants = data.get("variants", [])
        if not isinstance(raw_variants, list) or len(raw_variants) == 0:
            logger.warning("[variant_mapper] 'variants' ausente o vacío — usando fallback")
            return _make_fallback_variants()

        result: list[IdeaVariantItem] = []
        for item in raw_variants:
            variant_type = item.get("variant_type", "")
            if variant_type not in _VALID_TYPES:
                variant_type = "expansion"

            title = str(item.get("title", "Variant")).strip()[:60] or "Variant"
            content = str(item.get("content", "")).strip() or "No content provided."

            result.append(
                IdeaVariantItem(
                    variant_id=str(uuid.uuid4()),
                    title=title,
                    content=content,
                    variant_type=variant_type,  # type: ignore[arg-type]
                )
            )

        if len(result) >= 3:
            return result[:3]

        # Pad with fresh fallback items to always deliver exactly 3.
        needed = 3 - len(result)
        logger.warning(
            "[variant_mapper] Modelo devolvió %d variante(s) en lugar de 3 — completando con fallback",
            len(result),
        )
        fallback_items = _make_fallback_variants()[:needed]
        return result + fallback_items

    except (LLMParseError, AttributeError, TypeError) as exc:
        logger.warning("[variant_mapper] No se pudo parsear la respuesta: %s", exc)
        return _make_fallback_variants()
