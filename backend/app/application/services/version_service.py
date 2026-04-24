"""
version_service.py — Servicio de aplicación para IdeaVersions.

Gestiona el ciclo de vida completo de las versiones de una idea,
incluyendo transformaciones con IA a través de OllamaProvider.

Flujo de estados de una versión:
    DRAFT → ANALYZED → SELECTED → SUPERSEDED

CAMBIOS TAREA 3 (Fortalecer versionado):

1. get_latest_version() ahora usa el método del repositorio get_latest_by_idea_id()
   en lugar de traer todas las versiones y calcular el máximo en memoria.
   Más eficiente y preparado para cuando el repositorio esté en SQLite real.

2. Se añadió get_active_version() que usa VersionRules.get_active_version()
   para obtener la versión activa actual de una idea, no solo la más reciente.
   La diferencia: "más reciente" y "activa" no siempre son lo mismo si hay
   inconsistencias en el historial.

3. Se añadió get_version_lineage() que construye el árbol de trazabilidad
   completo de una idea usando get_lineage_info() de cada versión.
   Útil para synthesis_service y para debug del historial evolutivo.
"""

from typing import Optional

from app.domain.entities.idea_version import IdeaVersion
from app.domain.entities.idea_variant import IdeaVariant
from app.domain.repositories.idea_repository import IdeaRepository
from app.domain.repositories.version_repository import VersionRepository
from app.domain.rules.version_rules import VersionRules
from app.domain.value_objects.transformation_type import TransformationType
from app.infrastructure.ai.ollama_provider import OllamaProvider
from app.shared.database import db_wrapper


class VersionService:
    """
    Servicio que gestiona el ciclo de vida de las versiones de una idea.

    Dependencias:
    - VersionRepository: persistir y recuperar versiones.
    - IdeaRepository: verificar que la idea padre existe y obtener session_id.
    - OllamaProvider: generar contenido transformado con IA.
    """

    def __init__(
        self,
        version_repository: VersionRepository,
        idea_repository: IdeaRepository,
        ollama_provider: OllamaProvider,
    ) -> None:
        self._version_repo = version_repository
        self._idea_repo = idea_repository
        self._provider = ollama_provider

    # ──────────────────────────────────────────────────────────────────────────
    # CREAR VERSIONES
    # ──────────────────────────────────────────────────────────────────────────

    @db_wrapper
    async def create_initial_version(
        self,
        idea_id: str,
        title: str,
        content: str,
        **kwargs,
    ) -> IdeaVersion:
        """
        Crea la primera versión (v1) de una idea recién creada.

        Recupera la idea padre para obtener session_id, que IdeaVersion requiere
        como campo obligatorio. Sin esto, create_initial() lanza TypeError.
        """
        idea = await self._idea_repo.get_by_id(idea_id, kwargs["cursor"])
        if idea is None:
            raise ValueError(
                f"No se puede crear una versión: la idea '{idea_id}' no existe. "
                "Verifica que idea_service haya persistido la idea primero."
            )

        existing = await self._version_repo.get_by_idea_id(idea_id, kwargs["cursor"])
        if not VersionRules.can_create_next_version(existing):
            raise ValueError(
                f"La idea '{idea_id}' ya tiene el máximo de versiones permitidas "
                f"({VersionRules.MAX_VERSIONS_PER_IDEA}). Genera una síntesis antes de continuar."
            )

        version = IdeaVersion.create_initial(
            session_id=idea.session_id,
            idea_id=idea_id,
            title=title,
            content=content,
        )

        return await self._version_repo.save(version, kwargs["cursor"])

    @db_wrapper
    async def create_version_from_transformation(
        self,
        idea_id: str,
        parent_version_id: str,
        selected_variant: IdeaVariant,
        **kwargs,
    ) -> IdeaVersion:
        """
        Crea una nueva versión a partir de una variante seleccionada.
        Marca la versión padre como SUPERSEDED (cambia status e is_active).
        """
        parent_version = await self._version_repo.get_by_id(parent_version_id, kwargs["cursor"])
        if parent_version is None:
            raise ValueError(f"La versión padre '{parent_version_id}' no existe.")

        existing = await self._version_repo.get_by_idea_id(idea_id, kwargs["cursor"])
        if not VersionRules.can_create_next_version(existing):
            raise ValueError(
                f"La idea '{idea_id}' alcanzó el máximo de versiones permitidas. "
                "Genera una síntesis final antes de seguir iterando."
            )

        new_version = IdeaVersion.create_from_variant(
            idea_id=idea_id,
            parent_version=parent_version,
            selected_variant=selected_variant,
        )

        # supersede() ahora actualiza status e is_active en un solo paso.
        parent_version.supersede()
        await self._version_repo.save(parent_version, kwargs["cursor"])

        return await self._version_repo.save(new_version, kwargs["cursor"])

    # ──────────────────────────────────────────────────────────────────────────
    # TRANSFORMACIÓN CON IA
    # ──────────────────────────────────────────────────────────────────────────

    async def ai_transform(
        self,
        idea_id: str,
        parent_version_id: str,
        instruction: str,
        transformation_type: TransformationType,
        **kwargs,
    ) -> IdeaVersion:
        """
        Transformación con IA: llama a Ollama, construye la variante,
        crea la nueva versión y avanza su pipeline hasta SELECTED.

        Flujo:
        1. Obtiene la versión actual.
        2. Llama a Ollama para generar el contenido transformado.
        3. Construye IdeaVariant con el resultado.
        4. Crea nueva IdeaVersion (marca la padre como SUPERSEDED).
        5. DRAFT → ANALYZED → SELECTED.
        """
        current_version = await self.get_version(idea_id, parent_version_id, **kwargs)

        ai_result = await self._provider.transform_version(
            current_title=current_version.title,
            current_content=current_version.content,
            transformation_type=transformation_type.value,
            instruction=instruction,
        )

        transform_variant = IdeaVariant.create(
            version_id=current_version.id,
            title=ai_result["title"],
            content=ai_result["content"],
            transformation_type=transformation_type,
        )

        new_version = await self.create_version_from_transformation(
            idea_id=idea_id,
            parent_version_id=parent_version_id,
            selected_variant=transform_variant,
            **kwargs,
        )

        await self.mark_analyzed(idea_id, new_version.id, **kwargs)
        return await self.mark_selected(idea_id, new_version.id, **kwargs)

    # ──────────────────────────────────────────────────────────────────────────
    # OBTENER VERSIONES
    # ──────────────────────────────────────────────────────────────────────────

    @db_wrapper
    async def get_version(self, idea_id: str, version_id: str, **kwargs) -> IdeaVersion:
        """
        Retorna una versión específica validando que pertenece a la idea indicada.
        Lanza ValueError si no existe o no corresponde a esa idea.
        """
        version = await self._version_repo.get_by_id(version_id, kwargs["cursor"])
        if version is None or version.idea_id != idea_id:
            raise ValueError(
                f"La versión '{version_id}' no existe para la idea '{idea_id}'."
            )
        return version

    @db_wrapper
    async def get_latest_version(self, idea_id: str, **kwargs) -> Optional[IdeaVersion]:
        """
        Retorna la versión con el version_number más alto de una idea.

        MEJORA TAREA 3: ahora usa get_latest_by_idea_id() del repositorio
        en lugar de traer todas las versiones y calcular el máximo en memoria.
        Más eficiente y preparado para la implementación SQLite real.
        """
        return await self._version_repo.get_latest_by_idea_id(idea_id, kwargs["cursor"])

    @db_wrapper
    async def get_active_version(self, idea_id: str, **kwargs) -> Optional[IdeaVersion]:
        """
        Retorna la versión activa actual de una idea.

        NUEVO TAREA 3: usa VersionRules.get_active_version() que filtra
        por is_active y status. Diferente a get_latest_version() que solo
        mira el version_number más alto — una versión puede ser la más reciente
        pero no estar activa si hubo inconsistencias en el historial.

        Retorna None si todas las versiones están SUPERSEDED.
        """
        versions = await self._version_repo.get_by_idea_id(idea_id, kwargs["cursor"])
        return VersionRules.get_active_version(versions)

    @db_wrapper
    async def get_all_versions(self, idea_id: str, **kwargs) -> list[IdeaVersion]:
        """
        Retorna todas las versiones de una idea ordenadas por version_number.
        """
        versions = await self._version_repo.get_by_idea_id(idea_id, kwargs["cursor"])
        return sorted(versions, key=lambda v: v.version_number)

    @db_wrapper
    async def get_version_lineage(self, idea_id: str, **kwargs) -> list[dict]:
        """
        Retorna el árbol de trazabilidad completo de una idea.

        NUEVO TAREA 3: usa get_lineage_info() de cada IdeaVersion para
        construir el historial evolutivo completo ordenado por version_number.

        Útil para:
        - synthesis_service: construir el contexto que se pasa a la IA.
        - Debug: entender qué versión viene de cuál y por qué variante.

        Retorna una lista de dicts con la info de trazabilidad de cada versión.
        """
        versions = await self.get_all_versions(idea_id)
        return [v.get_lineage_info() for v in versions]

    # ──────────────────────────────────────────────────────────────────────────
    # AVANCE DE ESTADOS
    # ──────────────────────────────────────────────────────────────────────────

    @db_wrapper
    async def mark_analyzed(self, idea_id: str, version_id: str, **kwargs) -> IdeaVersion:
        """
        DRAFT → ANALYZED: la IA terminó de procesar esta versión.
        Si falla: la versión no está en DRAFT.
        """
        version = await self.get_version(idea_id, version_id)
        version.mark_analyzed()
        return await self._version_repo.save(version, kwargs["cursor"])

    @db_wrapper
    async def mark_selected(self, idea_id: str, version_id: str, **kwargs) -> IdeaVersion:
        """
        ANALYZED → SELECTED: el usuario eligió esta versión para avanzar.
        Si falla: la versión no está en ANALYZED todavía.
        """
        version = await self.get_version(idea_id, version_id)
        version.mark_selected()
        return await self._version_repo.save(version, kwargs["cursor"])

    # ──────────────────────────────────────────────────────────────────────────
    # VARIANTES
    # ──────────────────────────────────────────────────────────────────────────

    @db_wrapper
    async def add_variant_to_version(
        self,
        idea_id: str,
        version_id: str,
        variant: IdeaVariant,
        **kwargs,
    ) -> IdeaVersion:
        """
        Agrega una variante a una versión.
        IdeaVersion.add_variant() valida que esté en DRAFT o ANALYZED.
        """
        version = await self.get_version(idea_id, version_id)
        version.add_variant(variant)
        return await self._version_repo.save(version, kwargs["cursor"])

    # ──────────────────────────────────────────────────────────────────────────
    # UTILIDADES
    # ──────────────────────────────────────────────────────────────────────────

    async def assert_version_exists(self, idea_id: str, version_id: str, **kwargs) -> IdeaVersion:
        """Verifica que una versión existe. Utilitario para otros servicios."""
        return await self.get_version(idea_id, version_id, **kwargs)
