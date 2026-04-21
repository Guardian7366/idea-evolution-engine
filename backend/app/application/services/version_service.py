"""
version_service.py — Application service for IdeaVersions.

Manages the full lifecycle of idea versions including AI-powered transformations.

Flujo de estados de una versión:
    DRAFT → ANALYZED → SELECTED → SUPERSEDED
""""""
version_service.py — Servicio de aplicación para IdeaVersions.

Gestiona el ciclo de vida completo de las versiones de una idea,
incluyendo transformaciones con IA a través de OllamaProvider.

Flujo de estados de una versión:
    DRAFT → ANALYZED → SELECTED → SUPERSEDED

CAMBIOS RESPECTO A SEMANA 1:
- create_initial_version() ahora recupera la idea para obtener session_id
  y pasárselo a IdeaVersion.create_initial(), que lo requiere como campo
  obligatorio. Antes se omitía y causaba TypeError al instanciar la versión.
- Se eliminaron start_analysis() y mark_analysis_complete() porque
  VersionStatus no tiene ANALYZING — el pipeline real es DRAFT → ANALYZED directo.
- Se añadió ai_transform() que encapsula la llamada a OllamaProvider y el
  pipeline completo de una transformación con IA.
"""

from typing import Optional

from app.domain.entities.idea_version import IdeaVersion
from app.domain.entities.idea_variant import IdeaVariant
from app.domain.repositories.idea_repository import IdeaRepository
from app.domain.repositories.version_repository import VersionRepository
from app.domain.rules.version_rules import VersionRules
from app.domain.value_objects.transformation_type import TransformationType
from app.infrastructure.ai.ollama_provider import OllamaProvider


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

    async def create_initial_version(
        self,
        idea_id: str,
        title: str,
        content: str,
    ) -> IdeaVersion:
        """
        Crea la primera versión (v1) de una idea recién creada.

        CORRECCIÓN SEMANA 2: recuperamos la idea para obtener su session_id
        y pasárselo a IdeaVersion.create_initial(), que lo requiere.
        La versión anterior omitía session_id y causaba TypeError.

        Si lanza "idea no encontrada": idea_service no persistió la idea
        antes de llamar este método. Revisa el orden en idea_service.create_idea().
        """
        idea = await self._idea_repo.get_by_id(idea_id)
        if idea is None:
            raise ValueError(
                f"No se puede crear una versión: la idea '{idea_id}' no existe. "
                "Verifica que idea_service haya persistido la idea primero."
            )

        existing = await self._version_repo.get_by_idea_id(idea_id)
        if not VersionRules.can_create_next_version(existing):
            raise ValueError(
                f"La idea '{idea_id}' ya tiene el máximo de versiones permitidas "
                f"({VersionRules.MAX_VERSIONS_PER_IDEA}). Genera una síntesis antes de continuar."
            )

        # session_id viene de la idea padre — IdeaVersion lo necesita como campo propio.
        version = IdeaVersion.create_initial(
            session_id=idea.session_id,
            idea_id=idea_id,
            title=title,
            content=content,
        )

        return await self._version_repo.save(version)

    async def create_version_from_transformation(
        self,
        idea_id: str,
        parent_version_id: str,
        selected_variant: IdeaVariant,
    ) -> IdeaVersion:
        """
        Crea una nueva versión a partir de una variante seleccionada.
        También marca la versión padre como SUPERSEDED automáticamente.

        Si lanza "versión padre no encontrada": parent_version_id incorrecto.
        Si lanza "máximo de versiones": usar generate_final_synthesis primero.
        """
        parent_version = await self._version_repo.get_by_id(parent_version_id)
        if parent_version is None:
            raise ValueError(f"La versión padre '{parent_version_id}' no existe.")

        existing = await self._version_repo.get_by_idea_id(idea_id)
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

        # Marcamos la versión padre como reemplazada antes de persistir la nueva.
        # Si supersede() falla: la versión padre no puede ser reemplazada desde
        # su estado actual (ver VersionStatus.can_transition_to).
        parent_version.supersede()
        await self._version_repo.save(parent_version)

        return await self._version_repo.save(new_version)

    # ──────────────────────────────────────────────────────────────────────────
    # TRANSFORMACIÓN CON IA
    # ──────────────────────────────────────────────────────────────────────────

    async def ai_transform(
        self,
        idea_id: str,
        parent_version_id: str,
        instruction: str,
        transformation_type: TransformationType,
    ) -> IdeaVersion:
        """
        Transformación con IA: llama a Ollama, construye la variante,
        crea la nueva versión y avanza su pipeline hasta SELECTED.

        Flujo interno:
        1. Obtiene la versión actual.
        2. Llama a Ollama con el contenido actual y la instrucción.
        3. Construye IdeaVariant con el resultado.
        4. Crea nueva IdeaVersion (marca la padre como SUPERSEDED).
        5. DRAFT → ANALYZED → SELECTED.

        Si Ollama falla: OllamaProvider lanza su propia excepción.
        El endpoint debe capturarla y devolver un error apropiado al frontend.
        """
        current_version = await self.get_version(idea_id, parent_version_id)

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
        )

        # Pipeline: DRAFT → ANALYZED → SELECTED.
        # No hay ANALYZING en el sistema real — es un salto directo a ANALYZED.
        await self.mark_analyzed(idea_id, new_version.id)
        return await self.mark_selected(idea_id, new_version.id)

    # ──────────────────────────────────────────────────────────────────────────
    # OBTENER VERSIONES
    # ──────────────────────────────────────────────────────────────────────────

    async def get_version(self, idea_id: str, version_id: str) -> IdeaVersion:
        """
        Retorna una versión específica validando que pertenece a la idea indicada.
        Lanza ValueError si no existe o no corresponde a esa idea.
        """
        version = await self._version_repo.get_by_id(version_id)
        if version is None or version.idea_id != idea_id:
            raise ValueError(
                f"La versión '{version_id}' no existe para la idea '{idea_id}'."
            )
        return version

    async def get_latest_version(self, idea_id: str) -> Optional[IdeaVersion]:
        """
        Retorna la versión con el version_number más alto de una idea.
        Retorna None si la idea no tiene versiones todavía.
        """
        versions = await self._version_repo.get_by_idea_id(idea_id)
        return VersionRules.get_latest_version(versions)

    async def get_all_versions(self, idea_id: str) -> list[IdeaVersion]:
        """
        Retorna todas las versiones de una idea ordenadas por version_number.
        Usado por generate_final_synthesis para construir el contexto histórico.
        """
        versions = await self._version_repo.get_by_idea_id(idea_id)
        return sorted(versions, key=lambda v: v.version_number)

    # ──────────────────────────────────────────────────────────────────────────
    # AVANCE DE ESTADOS
    # ──────────────────────────────────────────────────────────────────────────

    async def mark_analyzed(self, idea_id: str, version_id: str) -> IdeaVersion:
        """
        Avanza la versión de DRAFT → ANALYZED.

        NOTA: el pipeline real no tiene ANALYZING.
        Los métodos start_analysis() y mark_analysis_complete() de Semana 1
        se eliminaron porque dependían de ese estado inexistente.

        Si falla: la versión no está en DRAFT.
        """
        version = await self.get_version(idea_id, version_id)
        version.mark_analyzed()
        return await self._version_repo.save(version)

    async def mark_selected(self, idea_id: str, version_id: str) -> IdeaVersion:
        """
        Avanza la versión de ANALYZED → SELECTED.
        Si falla: la versión no está en ANALYZED todavía.
        """
        version = await self.get_version(idea_id, version_id)
        version.mark_selected()
        return await self._version_repo.save(version)

    # ──────────────────────────────────────────────────────────────────────────
    # VARIANTES
    # ──────────────────────────────────────────────────────────────────────────

    async def add_variant_to_version(
        self,
        idea_id: str,
        version_id: str,
        variant: IdeaVariant,
    ) -> IdeaVersion:
        """
        Agrega una variante a una versión.
        IdeaVersion.add_variant() valida que la versión esté en DRAFT o ANALYZED.
        Si falla: la versión ya fue SELECTED o SUPERSEDED.
        """
        version = await self.get_version(idea_id, version_id)
        version.add_variant(variant)
        return await self._version_repo.save(version)

    # ──────────────────────────────────────────────────────────────────────────
    # UTILIDADES
    # ──────────────────────────────────────────────────────────────────────────

    async def assert_version_exists(self, idea_id: str, version_id: str) -> IdeaVersion:
        """Verifica que una versión existe. Utilitario para otros servicios."""
        return await self.get_version(idea_id, version_id)

from typing import Optional

from app.domain.entities.idea_version import IdeaVersion
from app.domain.entities.idea_variant import IdeaVariant
from app.domain.repositories.idea_repository import IdeaRepository
from app.domain.repositories.version_repository import VersionRepository
from app.domain.rules.version_rules import VersionRules
from app.domain.value_objects.transformation_type import TransformationType
from app.infrastructure.ai.ollama_provider import OllamaProvider


class VersionService:
    """
    Manages the lifecycle of idea versions.

    Receives three dependencies:
    - VersionRepository: persist and retrieve versions.
    - IdeaRepository: verify the parent idea exists before creating versions.
    - OllamaProvider: generate AI-powered transformation content.
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

    # ── CREATE VERSIONS ───────────────────────────────────────────────────────

    async def create_initial_version(
        self,
        idea_id: str,
        title: str,
        content: str,
    ) -> IdeaVersion:
        """Create the first version (v1) of a newly created idea."""
        idea = await self._idea_repo.get_by_id(idea_id)
        if idea is None:
            raise ValueError(
                f"No se puede crear una versión: la idea '{idea_id}' no existe. "
                "Verifica que idea_service haya persistido la idea primero."
            )

        existing = await self._version_repo.get_by_idea_id(idea_id)
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

        return await self._version_repo.save(version)

    async def create_version_from_transformation(
        self,
        idea_id: str,
        parent_version_id: str,
        selected_variant: IdeaVariant,
    ) -> IdeaVersion:
        """
        Create a new version from a selected variant.
        Also marks the parent version as SUPERSEDED.
        """
        parent_version = await self._version_repo.get_by_id(parent_version_id)
        if parent_version is None:
            raise ValueError(f"La versión padre '{parent_version_id}' no existe.")

        existing = await self._version_repo.get_by_idea_id(idea_id)
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

        parent_version.supersede()
        await self._version_repo.save(parent_version)

        return await self._version_repo.save(new_version)

    # ── AI TRANSFORM (called by idea_service) ─────────────────────────────────

    async def ai_transform(
        self,
        idea_id: str,
        parent_version_id: str,
        instruction: str,
        transformation_type: TransformationType,
    ) -> IdeaVersion:
        """
        AI-powered transformation: calls Ollama to generate new content,
        builds the IdeaVariant, creates the new version, and advances its pipeline.

        This is the method that owns 'version_service → transformaciones'.
        """
        current_version = await self.get_version(idea_id, parent_version_id)

        # Call Ollama to generate the transformed content.
        ai_result = await self._provider.transform_version(
            current_title=current_version.title,
            current_content=current_version.content,
            transformation_type=transformation_type.value,
            instruction=instruction,
        )

        # Build the IdeaVariant from the AI output.
        transform_variant = IdeaVariant.create(
            version_id=current_version.id,
            title=ai_result["title"],
            content=ai_result["content"],
            transformation_type=transformation_type,
        )

        # Create the new version (also supersedes the parent).
        new_version = await self.create_version_from_transformation(
            idea_id=idea_id,
            parent_version_id=parent_version_id,
            selected_variant=transform_variant,
        )

        # Advance the pipeline: DRAFT → ANALYZED → SELECTED.
        await self.mark_analyzed(idea_id, new_version.id)
        updated_version = await self.mark_selected(idea_id, new_version.id)

        return updated_version

    # ── GET VERSIONS ──────────────────────────────────────────────────────────

    async def get_version(self, idea_id: str, version_id: str) -> IdeaVersion:
        version = await self._version_repo.get_by_id(version_id)
        if version is None or version.idea_id != idea_id:
            raise ValueError(
                f"La versión '{version_id}' no existe para la idea '{idea_id}'."
            )
        return version

    async def get_latest_version(self, idea_id: str) -> Optional[IdeaVersion]:
        versions = await self._version_repo.get_by_idea_id(idea_id)
        return VersionRules.get_latest_version(versions)

    async def get_all_versions(self, idea_id: str) -> list[IdeaVersion]:
        versions = await self._version_repo.get_by_idea_id(idea_id)
        return sorted(versions, key=lambda v: v.version_number)

    # ── STATE TRANSITIONS ─────────────────────────────────────────────────────

    async def mark_analyzed(self, idea_id: str, version_id: str) -> IdeaVersion:
        version = await self.get_version(idea_id, version_id)
        version.mark_analyzed()
        return await self._version_repo.save(version)

    async def mark_selected(self, idea_id: str, version_id: str) -> IdeaVersion:
        version = await self.get_version(idea_id, version_id)
        version.mark_selected()
        return await self._version_repo.save(version)

    # ── VARIANTS ──────────────────────────────────────────────────────────────

    async def add_variant_to_version(
        self,
        idea_id: str,
        version_id: str,
        variant: IdeaVariant,
    ) -> IdeaVersion:
        version = await self.get_version(idea_id, version_id)
        version.add_variant(variant)
        return await self._version_repo.save(version)

    # ── UTILITIES ─────────────────────────────────────────────────────────────

    async def assert_version_exists(self, idea_id: str, version_id: str) -> IdeaVersion:
        return await self.get_version(idea_id, version_id)
