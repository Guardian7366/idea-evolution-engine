from enum import Enum


class VersionStatus(str, Enum):
    """
    Value Object que representa el estado de una versión de idea.
    Hereda de str para serialización directa a JSON.
    """
    DRAFT = "draft"
    ANALYZED = "analyzed"
    SELECTED = "selected"
    SUPERSEDED = "superseded"

    def can_transition_to(self, next_status: "VersionStatus") -> bool:
        """Define las transiciones de estado válidas para una versión."""
        allowed: dict[VersionStatus, set[VersionStatus]] = {
            VersionStatus.DRAFT: {VersionStatus.ANALYZED},
            VersionStatus.ANALYZED: {VersionStatus.SELECTED, VersionStatus.SUPERSEDED},
            VersionStatus.SELECTED: {VersionStatus.SUPERSEDED},
            VersionStatus.SUPERSEDED: set(),
        }
        return next_status in allowed[self]

    def is_active(self) -> bool:
        """Una versión está activa si no ha sido reemplazada."""
        return self != VersionStatus.SUPERSEDED