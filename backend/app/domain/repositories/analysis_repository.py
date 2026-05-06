from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.version_analysis import VersionAnalysis
from app.domain.entities.version_comparison import VersionComparison


class AnalysisRepository(ABC):
    @abstractmethod
    def save_analysis(self, analysis: VersionAnalysis) -> VersionAnalysis:
        raise NotImplementedError

    @abstractmethod
    def save_comparison(self, comparison: VersionComparison) -> VersionComparison:
        raise NotImplementedError