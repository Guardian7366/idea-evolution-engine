from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.value_objects.idea_content import IdeaContent
from app.domain.value_objects.transformation_type import TransformationType


@dataclass
class IdeaVariant:
    """
    Entidad que representa una variante generada de una idea.
    Una variante es el resultado de aplicar una transformación
    (mutación, refinamiento, expansión, etc.) a una versión de idea.
    Pertenece siempre a una IdeaVersion.
    """
    id: str
    version_id: str
    content: IdeaContent
    transformation_type: TransformationType
    is_selected: bool
    created_at: datetime

    @classmethod
    def create(
        cls,
        version_id: str,
        title: str,
        description: str,
        transformation_type: TransformationType,
        variant_id: str | None = None,  # ✅ nuevo
    ) -> "IdeaVariant":
        """
        Factory method. Crea una variante nueva asociada a una versión.

        IMPORTANTE:
        Permite recibir variant_id externo (desde IA/frontend)
        para mantener trazabilidad consistente en todo el sistema.
        """
        return cls(
            id=variant_id if variant_id is not None else str(uuid4()),
            version_id=version_id,
            content=IdeaContent(title=title, description=description),
            transformation_type=transformation_type,
            is_selected=False,
            created_at=datetime.now(timezone.utc),
        )

    def select(self) -> None:
        """Marca esta variante como la seleccionada por el usuario."""
        self.is_selected = True

    def deselect(self) -> None:
        """Desmarca esta variante."""
        self.is_selected = False