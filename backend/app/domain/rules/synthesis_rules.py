from __future__ import annotations

from app.domain.entities.final_synthesis import FinalSynthesis


def ensure_synthesis_is_complete(synthesis: FinalSynthesis) -> None:
    fields = [
        synthesis.summary,
        synthesis.value_proposition,
        synthesis.target_audience,
        synthesis.structured_description,
        synthesis.next_steps,
    ]
    if any(not field.strip() for field in fields):
        raise ValueError("Final synthesis fields cannot be empty.")