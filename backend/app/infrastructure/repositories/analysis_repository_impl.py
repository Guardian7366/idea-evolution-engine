from __future__ import annotations

from sqlalchemy.orm import Session as DBSession

from app.domain.entities.version_analysis import VersionAnalysis
from app.domain.entities.version_comparison import VersionComparison
from app.domain.repositories.analysis_repository import AnalysisRepository
from app.infrastructure.persistence.models.analysis_model import (
    VersionAnalysisModel,
    VersionComparisonModel,
)


class SqliteAnalysisRepository(AnalysisRepository):
    def __init__(self, db: DBSession) -> None:
        self.db = db

    def save_analysis(self, analysis: VersionAnalysis) -> VersionAnalysis:
        model = VersionAnalysisModel(
            id=analysis.id,
            version_id=analysis.version_id,
            analysis_type=analysis.analysis_type,
            content=analysis.content,
            created_at=analysis.created_at.isoformat(),
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return analysis

    def save_comparison(self, comparison: VersionComparison) -> VersionComparison:
        model = VersionComparisonModel(
            id=comparison.id,
            idea_id=comparison.idea_id,
            left_version_id=comparison.left_version_id,
            right_version_id=comparison.right_version_id,
            comparison_text=comparison.comparison_text,
            created_at=comparison.created_at.isoformat(),
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return comparison