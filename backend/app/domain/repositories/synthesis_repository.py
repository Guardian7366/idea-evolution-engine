from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.final_synthesis import FinalSynthesis


class SynthesisRepository(ABC):
    @abstractmethod
    def save(self, synthesis: FinalSynthesis) -> FinalSynthesis:
        raise NotImplementedError