from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IdeaContent:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("Idea content cannot be empty.")

        if len(normalized) > 2000:
            raise ValueError("Idea content cannot exceed 2000 characters.")

        object.__setattr__(self, "value", normalized)