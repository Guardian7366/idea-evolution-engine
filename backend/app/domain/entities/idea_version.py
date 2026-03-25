from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.domain.value_objects.idea_content import IdeaContent
from app.domain.value_objects.version_status import VersionStatus
from app.domain.value_objects.transformation_type import TransformationType
from app.domain.entities.idea_variant import IdeaVariant


@dataclass
class IdeaVersion:
    """
    Entidad que representa una versión específica de una idea.
    Cada vez que una idea evoluciona (por selección de variante,
    refinamiento, etc.), se genera una nueva versión.
    El historial de versiones conforma la "evolución" de la idea.
    """
    id: str
    idea_id: str
    version_number: int
    content: IdeaContent
    status: VersionStatus
    parent_version_id: Optional[str]
    created_at: datetime
    variants: list[IdeaVariant] = field(default_factory=list)

    @classmethod
    def create_initial(cls, idea_id: str, title: str, description: str) -> "IdeaVersion":
        """Factory: crea la primera versión de una idea (v1, sin parent)."""
        return cls(
            id=str(uuid4()),
            idea_id=idea_id,
            version_number=1,
            content=IdeaContent(title=title, description=description),
            status=VersionStatus.DRAFT,
            parent_version_id=None,
            created_at=datetime.now(timezone.utc),
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
        return cls(
            id=str(uuid4()),
            idea_id=idea_id,
            version_number=parent_version.version_number + 1,
            content=selected_variant.content,
            status=VersionStatus.DRAFT,
            parent_version_id=parent_version.id,
            created_at=datetime.now(timezone.utc),
        )

    def add_variant(self, variant: IdeaVariant) -> None:
        """Agrega una variante generada a esta versión."""
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