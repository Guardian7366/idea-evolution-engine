from __future__ import annotations

from sqlalchemy.orm import Session as DBSession

from app.domain.entities.final_synthesis import FinalSynthesis
from app.domain.repositories.synthesis_repository import SynthesisRepository
from app.infrastructure.persistence.models.synthesis_model import FinalSynthesisModel


class SqliteSynthesisRepository(SynthesisRepository):
    def __init__(self, db: DBSession) -> None:
        self.db = db

    def save(self, synthesis: FinalSynthesis) -> FinalSynthesis:
        model = FinalSynthesisModel(
            id=synthesis.id,
            idea_id=synthesis.idea_id,
            version_id=synthesis.version_id,
            summary=synthesis.summary,
            value_proposition=synthesis.value_proposition,
            target_audience=synthesis.target_audience,
            structured_description=synthesis.structured_description,
            next_steps=synthesis.next_steps,
            created_at=synthesis.created_at.isoformat(),
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return synthesis