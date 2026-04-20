from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.value_objects.session_status import SessionStatus
from app.domain.entities import DateHelper


@dataclass
class Session(DateHelper):
    """
    Entidad que representa una sesión de evolución de ideas.
    Una sesión agrupa todas las ideas que el usuario trabaja en
    una misma "run" de Idea Evolution Engine.
    """
    id: str
    title: str
    status: SessionStatus
    created_at: datetime
    updated_at: datetime
    idea_ids: list[str] = field(default_factory=list)

    @classmethod
    def create(cls, title: str) -> "Session":
        """Factory method. Crea una sesión nueva en estado ACTIVE."""
        if not title or not title.strip():
            raise ValueError("El título de la sesión no puede estar vacío.")
        now = datetime.now(timezone.utc)
        return cls(
            id=str(uuid4()),
            title=title.strip(),
            status=SessionStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )

    def add_idea(self, idea_id: str) -> None:
        """Registra una idea dentro de esta sesión."""
        self.ensure_active()
        if idea_id not in self.idea_ids:
            self.idea_ids.append(idea_id)
            self.updated_at = datetime.now(timezone.utc)

    def pause(self) -> None:
        self._transition_to(SessionStatus.PAUSED)

    def resume(self) -> None:
        self._transition_to(SessionStatus.ACTIVE)

    def complete(self) -> None:
        self._transition_to(SessionStatus.COMPLETED)

    def archive(self) -> None:
        self._transition_to(SessionStatus.ARCHIVED)

    def ensure_active(self) -> None:
        """Lanza excepción si la sesión no está activa."""
        if not self.status.is_editable():
            raise ValueError(
                f"La sesión '{self.id}' no está activa (estado: {self.status}). "
                "No se puede operar sobre ella."
            )

    def _transition_to(self, next_status: SessionStatus) -> None:
        if not self.status.can_transition_to(next_status):
            raise ValueError(
                f"Transición inválida: {self.status} → {next_status} "
                f"para la sesión '{self.id}'."
            )
        self.status = next_status
        self.updated_at = datetime.now(timezone.utc)
