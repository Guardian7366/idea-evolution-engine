from __future__ import annotations

from app.domain.entities.final_synthesis import FinalSynthesis


def map_synthesis_payload_to_entity(
    payload: dict,
    *,
    idea_id: str,
    version_id: str,
) -> FinalSynthesis:
    return FinalSynthesis(
        id=payload["id"],
        idea_id=idea_id,
        version_id=version_id,
        summary=payload["summary"],
        value_proposition=payload["value_proposition"],
        target_audience=payload["target_audience"],
        structured_description=payload["structured_description"],
        next_steps=payload["next_steps"],
        created_at=payload["created_at"],
    )