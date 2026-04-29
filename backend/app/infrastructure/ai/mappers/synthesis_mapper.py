"""
synthesis_mapper.py — Maps raw Ollama JSON output to FinalSynthesisResult DTO.

Called by: ollama_provider.py → generate_synthesis
"""

import logging

from app.application.dto.synthesis_dto import FinalSynthesisResult
from app.infrastructure.ai.mappers.base import LLMParseError, coerce_str_list, extract_json

logger = logging.getLogger(__name__)


def map_synthesis(raw_json: str, total_versions: int) -> FinalSynthesisResult:
    """
    Parse Ollama's JSON and return a FinalSynthesisResult.
    Falls back to a generic result on parse failure, with a warning log.
    """
    try:
        data = extract_json(raw_json)

        title = str(data.get("title", "")).strip()
        core_concept = str(data.get("core_concept", "")).strip()
        value_proposition = str(data.get("value_proposition", "")).strip()
        next_step = str(data.get("recommended_next_step", "")).strip()
        notes = coerce_str_list(data.get("notes"))

        if title and core_concept and value_proposition and next_step and notes:
            return FinalSynthesisResult(
                title=title[:80],
                core_concept=core_concept,
                value_proposition=value_proposition,
                recommended_next_step=next_step,
                notes=notes,
            )

        logger.warning(
            "[synthesis_mapper] Respuesta incompleta — "
            "title=%s  concept=%s  vp=%s  step=%s  notes=%d",
            bool(title), bool(core_concept), bool(value_proposition),
            bool(next_step), len(notes),
        )

    except (LLMParseError, AttributeError, TypeError) as exc:
        logger.warning("[synthesis_mapper] No se pudo parsear: %s", exc)

    return FinalSynthesisResult(
        title="Final Idea Synthesis",
        core_concept="The idea has evolved through multiple iterations and reached a refined state.",
        value_proposition="This concept delivers clear value to its target users through focused execution.",
        recommended_next_step="Build the simplest working version of the core loop and validate with real users.",
        notes=[
            f"This idea evolved through {total_versions} version(s) before synthesis.",
            "Keep the first release focused on validating the core value proposition.",
            "Preserve the evolution history to track decision-making over time.",
        ],
    )
