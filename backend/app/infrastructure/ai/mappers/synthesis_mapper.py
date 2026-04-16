"""
synthesis_mapper.py — Maps raw Ollama JSON output to FinalSynthesisResult DTO.

Called by: ollama_provider.py → generate_synthesis
"""

import json

from app.application.dto.synthesis_dto import FinalSynthesisResult


def map_synthesis(raw_json: str, total_versions: int) -> FinalSynthesisResult:
    """
    Parse Ollama's JSON and return a FinalSynthesisResult.
    Falls back to a generic result on parse failure.
    """
    try:
        data = json.loads(raw_json)

        title = str(data.get("title", "")).strip()
        core_concept = str(data.get("core_concept", "")).strip()
        value_proposition = str(data.get("value_proposition", "")).strip()
        next_step = str(data.get("recommended_next_step", "")).strip()
        notes = _coerce_list(data.get("notes"))

        if title and core_concept and value_proposition and next_step and notes:
            return FinalSynthesisResult(
                title=title[:80],
                core_concept=core_concept,
                value_proposition=value_proposition,
                recommended_next_step=next_step,
                notes=notes,
            )

    except (json.JSONDecodeError, AttributeError, TypeError):
        pass

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


def _coerce_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []
