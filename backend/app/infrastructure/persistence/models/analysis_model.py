from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String

from app.infrastructure.persistence.database import Base


class VersionAnalysisModel(Base):
    __tablename__ = "version_analyses"

    id = Column(String, primary_key=True, index=True)
    version_id = Column(String, ForeignKey("idea_versions.id"), nullable=False, index=True)
    analysis_type = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(String, nullable=False)


class VersionComparisonModel(Base):
    __tablename__ = "version_comparisons"

    id = Column(String, primary_key=True, index=True)
    idea_id = Column(String, ForeignKey("ideas.id"), nullable=False, index=True)
    left_version_id = Column(String, ForeignKey("idea_versions.id"), nullable=False)
    right_version_id = Column(String, ForeignKey("idea_versions.id"), nullable=False)
    comparison_text = Column(String, nullable=True)
    created_at = Column(String, nullable=False)