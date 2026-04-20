"""
version_service.py — Application service for IdeaVersions.

Manages the full lifecycle of idea versions including AI-powered transformations.

Flujo de estados de una versión:
    DRAFT → ANALYZED → SELECTED → SUPERSEDED
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
