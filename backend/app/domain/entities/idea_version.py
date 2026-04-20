from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal, Optional
from uuid import uuid4

from app.domain.value_objects.version_status import VersionStatus
from app.domain.entities.idea_variant import IdeaVariant
from app.domain.entities import DateHelper


@dataclass
class IdeaVersion(DateHelper):
    """
    Entidad que representa una versión específica de una idea.
    Cada vez que una idea evoluciona (por selección de variante,
    refinamiento, etc.), se genera una nueva versión.
    El historial de versiones conforma la "evolución" de la idea.
    """
    id: str
    session_id: str
    idea_id: str
    version_number: int
    title: str
    content: str
    status: VersionStatus
    is_active: Literal[0, 1]
    parent_version_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    variants: list[IdeaVariant] = field(default_factory=list)

    @classmethod
    def create_initial(cls, session_id: str, idea_id: str, title: str, content: str) -> "IdeaVersion":
        """Factory: crea la primera versión de una idea (v1, sin parent)."""
        return cls(
            id=str(uuid4()),
            session_id=session_id,
            idea_id=idea_id,
            version_number=1,
            title=title,
            content=content,
            status=VersionStatus.DRAFT,
            is_active=1,
            parent_version_id=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    @classmethod
    def create_from_variant(
        cls,
        idea_id: str,
        parent_version: "IdeaVersion",
        selected_variant: IdeaVariant,
    ) -> "IdeaVersion":
        """
        Factory: crea una nueva versión a partir de una variante seleccionada.
        El número de versión se incrementa automáticamente.
        """
        # IMPORTANTE:
        # Se clona el contenido para evitar referencias compartidas entre versiones.
        # Cada versión debe ser inmutable respecto a otras.
        return cls(
            id=str(uuid4()),
            idea_id=idea_id,
            version_number=parent_version.version_number + 1,
            title=selected_variant.title,
            content=selected_variant.content,
            status=VersionStatus.DRAFT,
            parent_version_id=parent_version.id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    def add_variant(self, variant: IdeaVariant) -> None:
        """
        Agrega una variante generada a esta versión.

        IMPORTANTE:
        Solo se permite agregar variantes en estado DRAFT o ANALYZED.
        Evita inconsistencias si la versión ya fue seleccionada o reemplazada.
        """
        if self.status not in (VersionStatus.DRAFT, VersionStatus.ANALYZED):
            raise ValueError(
                f"No se pueden agregar variantes a una versión en estado '{self.status}'."
            )

        self.variants.append(variant)

    def mark_analyzed(self) -> None:
        """Transiciona el estado a ANALYZED tras procesar con IA."""
        self._transition_to(VersionStatus.ANALYZED)

    def mark_selected(self) -> None:
        """El usuario eligió esta versión como punto de avance."""
        self._transition_to(VersionStatus.SELECTED)

    def supersede(self) -> None:
        """Esta versión fue reemplazada por una más nueva."""
        self._transition_to(VersionStatus.SUPERSEDED)

    def get_selected_variant(self) -> Optional[IdeaVariant]:
        """Retorna la variante seleccionada, si existe."""
        return next((v for v in self.variants if v.is_selected), None)

    def _transition_to(self, next_status: VersionStatus) -> None:
        if not self.status.can_transition_to(next_status):
            raise ValueError(
                f"Transición inválida: {self.status} → {next_status} "
                f"para la versión '{self.id}'."
            )
        self.status = next_status
