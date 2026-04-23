"""
idea_version.py — Entidad que representa una versión de una idea.

CAMBIOS TAREA 3 (Fortalecer versionado):

1. supersede() ahora actualiza is_active = 0 además de cambiar el status.
   Antes solo cambiaba status a SUPERSEDED pero dejaba is_active = 1,
   causando inconsistencia entre ambos campos.

2. Se añadió is_currently_active() — método semántico que combina is_active
   y status. Antes había que verificar ambos campos desde el servicio.

3. Se añadió get_lineage_info() — retorna un dict con la trazabilidad completa
   de esta versión (número, padre, origen de variante, estado).
   Útil para synthesis_service al construir el historial evolutivo.

4. add_variant() ahora actualiza updated_at al agregar una variante.

5. _transition_to() ahora actualiza updated_at en cada transición.
"""

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
    Cada evolución de la idea genera una nueva versión.
    El historial de versiones conforma la cadena evolutiva completa.
    """
    id: str
    session_id: str
    idea_id: str
    version_number: int
    title: str
    content: str
    status: VersionStatus

    # Flag de versión activa. 1 = activa, 0 = reemplazada.
    # Se mantiene sincronizado con status en todo momento:
    # - is_active=1 + status DRAFT/ANALYZED/SELECTED → versión en proceso
    # - is_active=0 + status SUPERSEDED → versión histórica, reemplazada
    is_active: Literal[0, 1]

    # ID de la variante que originó esta versión.
    # None en v1. En versiones derivadas apunta a la IdeaVariant elegida,
    # permitiendo rastrear por qué se tomó cada dirección evolutiva.
    source_variant_id: Optional[str]

    # ID de la versión anterior en la cadena evolutiva.
    # None en v1. Para versiones derivadas permite navegar: v3 → v2 → v1.
    parent_version_id: Optional[str]

    created_at: datetime
    updated_at: datetime

    # Variantes generadas en este ciclo evolutivo.
    # Se pueblan cuando la IA analiza la versión y genera opciones.
    variants: list[IdeaVariant] = field(default_factory=list)

    @classmethod
    def create_initial(
        cls, session_id: str, idea_id: str, title: str, content: str
    ) -> "IdeaVersion":
        """Factory: crea la primera versión de una idea (v1, sin parent)."""
        now = datetime.now(timezone.utc)
        return cls(
            id=str(uuid4()),
            session_id=session_id,
            idea_id=idea_id,
            version_number=1,
            title=title,
            content=content,
            status=VersionStatus.DRAFT,
            is_active=1,
            source_variant_id=None,
            parent_version_id=None,
            created_at=now,
            updated_at=now,
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

        - Hereda session_id del padre.
        - version_number se incrementa automáticamente.
        - source_variant_id y parent_version_id garantizan trazabilidad completa.
        """
        now = datetime.now(timezone.utc)
        return cls(
            id=str(uuid4()),
            session_id=parent_version.session_id,
            idea_id=idea_id,
            version_number=parent_version.version_number + 1,
            title=selected_variant.title,
            content=selected_variant.content,
            status=VersionStatus.DRAFT,
            is_active=1,
            source_variant_id=selected_variant.id,
            parent_version_id=parent_version.id,
            created_at=now,
            updated_at=now,
        )

    def add_variant(self, variant: IdeaVariant) -> None:
        """
        Agrega una variante generada a esta versión.
        Solo se permite en DRAFT o ANALYZED.
        """
        if self.status not in (VersionStatus.DRAFT, VersionStatus.ANALYZED):
            raise ValueError(
                f"No se pueden agregar variantes a una versión en estado '{self.status.value}'."
            )
        self.variants.append(variant)
        self.updated_at = datetime.now(timezone.utc)

    def mark_analyzed(self) -> None:
        """DRAFT → ANALYZED: la IA terminó de procesar esta versión."""
        self._transition_to(VersionStatus.ANALYZED)

    def mark_selected(self) -> None:
        """ANALYZED → SELECTED: el usuario eligió esta versión para avanzar."""
        self._transition_to(VersionStatus.SELECTED)

    def supersede(self) -> None:
        """
        Marca esta versión como reemplazada por una más nueva.

        Actualiza AMBOS campos para mantener consistencia:
        - status → SUPERSEDED
        - is_active → 0

        Si solo se actualizara status sin is_active, las queries que filtran
        por is_active=1 seguirían devolviendo esta versión como activa
        aunque ya fue reemplazada.
        """
        self._transition_to(VersionStatus.SUPERSEDED)
        self.is_active = 0

    def is_currently_active(self) -> bool:
        """
        ¿Esta versión es la activa actual de su idea?

        Combina is_active y status para una respuesta semántica clara.
        Una versión es activa si no fue marcada como reemplazada por ninguno
        de los dos mecanismos de trazabilidad.
        """
        return self.is_active == 1 and self.status != VersionStatus.SUPERSEDED

    def get_selected_variant(self) -> Optional[IdeaVariant]:
        """Retorna la variante seleccionada por el usuario, si existe."""
        return next((v for v in self.variants if v.is_selected), None)

    def get_lineage_info(self) -> dict:
        """
        Retorna la información de trazabilidad de esta versión.

        Usado por synthesis_service para construir el historial evolutivo
        sin acceder a campos individuales desde fuera de la entidad.
        Permite saber qué versión viene de cuál y por qué variante.
        """
        return {
            "version_id": self.id,
            "version_number": self.version_number,
            "status": self.status.value,
            "is_active": self.is_active,
            "parent_version_id": self.parent_version_id,
            "source_variant_id": self.source_variant_id,
            "title": self.title,
        }

    def _transition_to(self, next_status: VersionStatus) -> None:
        """Valida y aplica una transición de estado. Actualiza updated_at."""
        if not self.status.can_transition_to(next_status):
            raise ValueError(
                f"Transición inválida: {self.status.value} → {next_status.value} "
                f"para la versión '{self.id}'."
            )
        self.status = next_status
        self.updated_at = datetime.now(timezone.utc)