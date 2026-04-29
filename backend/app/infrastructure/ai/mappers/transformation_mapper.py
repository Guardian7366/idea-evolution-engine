"""
transformation_mapper.py — Maps raw Ollama JSON output to transformation content.

Called by: ollama_provider.py → transform_version
Returns a dict with 'title' and 'content' keys used to build the IdeaVariant.
"""

import logging

from app.infrastructure.ai.mappers.base import LLMParseError, extract_json

logger = logging.getLogger(__name__)

_TYPE_LABELS: dict[str, str] = {
    "evolve": "Evolved",
    "refine": "Refined",
    "mutate": "Mutated",
}


def map_transformation(raw_json: str, transformation_type: str, instruction: str) -> dict[str, str]:
    """
    Parse Ollama's JSON response and return {'title': ..., 'content': ...}.

    Falls back to a minimal result derived from the instruction itself,
    and logs a warning so the fallback is not invisible.
    """
    try:
        data = extract_json(raw_json)
        title = str(data.get("title", "")).strip()
        content = str(data.get("content", "")).strip()

        if title and content:
            return {"title": title[:80], "content": content}

        logger.warning(
            "[transformation_mapper] Respuesta incompleta — title=%s content=%s",
            bool(title), bool(content),
        )

    except (LLMParseError, AttributeError, TypeError) as exc:
        logger.warning("[transformation_mapper] No se pudo parsear: %s", exc)

    prefix = _TYPE_LABELS.get(transformation_type, "Transformed")
    return {
        "title": f"{prefix} Version",
        "content": f"Transformation ({transformation_type}): {instruction.rstrip('. ')}.",
    }
