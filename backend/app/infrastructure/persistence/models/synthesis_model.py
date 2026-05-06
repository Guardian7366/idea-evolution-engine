from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String

from app.infrastructure.persistence.database import Base


class FinalSynthesisModel(Base):
    __tablename__ = "final_syntheses"

    id = Column(String, primary_key=True, index=True)
    idea_id = Column(String, ForeignKey("ideas.id"), nullable=False, index=True)
    version_id = Column(String, ForeignKey("idea_versions.id"), nullable=False, index=True)
    summary = Column(String, nullable=False)
    value_proposition = Column(String, nullable=False)
    target_audience = Column(String, nullable=False)
    structured_description = Column(String, nullable=False)
    next_steps = Column(String, nullable=False)
    created_at = Column(String, nullable=False)