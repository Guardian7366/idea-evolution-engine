from enum import Enum


class SessionStatus(str, Enum):
    """
    Value Object que representa el estado del ciclo de vida de una sesión.
    Hereda de str para serialización directa a JSON sin configuración extra.
    """
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"

    def can_transition_to(self, next_status: "SessionStatus") -> bool:
        """Define las transiciones de estado permitidas."""
        allowed: dict[SessionStatus, set[SessionStatus]] = {
            SessionStatus.ACTIVE: {SessionStatus.PAUSED, SessionStatus.COMPLETED},
            SessionStatus.PAUSED: {SessionStatus.ACTIVE, SessionStatus.ARCHIVED},
            SessionStatus.COMPLETED: {SessionStatus.ARCHIVED},
            SessionStatus.ARCHIVED: set(),
        }
        return next_status in allowed[self]

    def is_editable(self) -> bool:
        """Una sesión solo es editable si está activa."""
        return self == SessionStatus.ACTIVE