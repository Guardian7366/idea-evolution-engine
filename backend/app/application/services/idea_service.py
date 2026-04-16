"""
idea_service.py — Application service that orchestrates the full idea evolution flow.

AI operations are delegated to specialized services:
  - generate_variants  → OllamaProvider (called directly here)
  - compare_versions   → AnalysisService
  - explore_perspective → AnalysisService
  - generate_final_synthesis → SynthesisService

transform_version orchestration stays here; the AI call inside it lives in VersionService.
"""

from typing import TYPE_CHECKING

from app.application.dto.comparison_dto import (
    CompareVersionsRequest,
    CompareVersionsResponse,
)
from app.application.dto.idea_dto import (
    IdeaCreateRequest,
    IdeaCreateResponse,
)
from app.application.dto.perspective_dto import (
    ExplorePerspectiveRequest,
    ExplorePerspectiveResponse,
)
from app.application.dto.selection_dto import (
    SelectVariantRequest,
    SelectVariantResponse,
)
from app.application.dto.synthesis_dto import (
    GenerateFinalSynthesisRequest,
    GenerateFinalSynthesisResponse,
)
from app.application.dto.transformation_dto import (
    TransformVersionRequest,
    TransformVersionResponse,
)
from app.application.dto.variant_dto import (
    GenerateVariantsRequest,
    GenerateVariantsResponse,
)
from app.application.dto.version_dto import ActiveIdeaVersion
from app.application.services.session_service import SessionService
from app.application.services.version_service import VersionService
from app.domain.entities.idea import Idea
from app.domain.entities.idea_variant import IdeaVariant
from app.domain.repositories.idea_repository import IdeaRepository
from app.domain.value_objects.transformation_type import TransformationType
from app.infrastructure.ai.ollama_provider import OllamaProvider

if TYPE_CHECKING:
    from app.application.services.analysis_service import AnalysisService
    from app.application.services.synthesis_service import SynthesisService


def _build_title_from_prompt(prompt: str, max_length: int = 60) -> str:
    stripped = prompt.strip()
    if len(stripped) <= max_length:
        return stripped
    truncated = stripped[:max_length].rsplit(' ', 1)[0]
    return f"{truncated}..."


class IdeaService:
    """
    Application service that orchestrates the complete idea evolution flow.
    """

    def __init__(
        self,
        idea_repository: IdeaRepository,
        session_service: SessionService,
        version_service: VersionService,
        ollama_provider: OllamaProvider,
        analysis_service: "AnalysisService",
        synthesis_service: "SynthesisService",
    ) -> None:
        self._idea_repo = idea_repository
        self._session_service = session_service
        self._version_service = version_service
        self._provider = ollama_provider
        self._analysis_service = analysis_service
        self._synthesis_service = synthesis_service

    # ── 1. CREATE IDEA ────────────────────────────────────────────────────────

    async def create_idea(self, payload: IdeaCreateRequest) -> IdeaCreateResponse:
        await self._session_service.assert_session_is_active(payload.session_id)

        title = _build_title_from_prompt(payload.initial_prompt)

        idea = Idea.create(
            session_id=payload.session_id,
            title=title,
            description=payload.initial_prompt,
        )
        persisted_idea = await self._idea_repo.save(idea)

        await self._session_service.register_idea_added(
            payload.session_id, persisted_idea.id
        )

        await self._version_service.create_initial_version(
            idea_id=persisted_idea.id,
            title=title,
            description=payload.initial_prompt,
        )

        return IdeaCreateResponse(
            idea_id=persisted_idea.id,
            session_id=payload.session_id,
            initial_prompt=payload.initial_prompt,
            message="Idea created successfully",
        )

    # ── 2. GENERATE VARIANTS (AI) ─────────────────────────────────────────────

    async def generate_variants(
        self,
        payload: GenerateVariantsRequest,
    ) -> GenerateVariantsResponse:
        """Generate variants using Ollama (Qwen2.5)."""
        idea = await self._idea_repo.get_by_id(payload.idea_id)
        if idea is None:
            raise ValueError(
                f"No se pueden generar variantes: la idea '{payload.idea_id}' no existe."
            )

        variants = await self._provider.generate_variants(payload.initial_prompt)

        return GenerateVariantsResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            variants=variants,
            message="Variants generated successfully",
        )

    # ── 3. SELECT VARIANT ─────────────────────────────────────────────────────

    async def select_variant(
        self,
        payload: SelectVariantRequest,
    ) -> SelectVariantResponse:
        """
        The user picks one variant. Creates the first real active version.
        variant_id is the UUID returned by generate_variants (from the AI).
        """
        idea = await self._idea_repo.get_by_id(payload.idea_id)
        if idea is None:
            raise ValueError(f"La idea '{payload.idea_id}' no existe.")

        latest_version = await self._version_service.get_latest_version(payload.idea_id)
        if latest_version is None:
            raise ValueError(
                f"La idea '{payload.idea_id}' no tiene versiones. "
                "Verifica que create_idea() se ejecutó correctamente."
            )

        variant = IdeaVariant.create(
            version_id=latest_version.id,
            title=payload.variant_title,
            description=payload.variant_content,
            transformation_type=TransformationType.SELECTION,
        )

        await self._version_service.mark_analyzed(payload.idea_id, latest_version.id)
        await self._version_service.add_variant_to_version(payload.idea_id, latest_version.id, variant)
        updated_version = await self._version_service.mark_selected(payload.idea_id, latest_version.id)

        active_version = ActiveIdeaVersion(
            version_id=updated_version.id,
            idea_id=payload.idea_id,
            session_id=payload.session_id,
            title=payload.variant_title,
            content=payload.variant_content,
            status="active",
            version_number=updated_version.version_number,
            parent_version_id=updated_version.parent_version_id,
            source_variant_id=variant.id,
            transformation_type=TransformationType.SELECTION.value,
        )

        return SelectVariantResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            selected_variant_id=payload.variant_id,
            active_version=active_version,
            message="Variant selected and active version created successfully",
        )

    # ── 4. TRANSFORM VERSION (AI via VersionService) ──────────────────────────

    async def transform_version(
        self,
        payload: TransformVersionRequest,
    ) -> TransformVersionResponse:
        """
        Orchestrates an AI-powered transformation of the current active version.
        The actual AI call and new version creation live in VersionService.
        """
        try:
            transformation = TransformationType(payload.transformation_type)
        except ValueError:
            raise ValueError(
                f"Tipo de transformación desconocido: '{payload.transformation_type}'. "
                f"Los valores válidos son: {[t.value for t in TransformationType]}."
            )

        new_version = await self._version_service.ai_transform(
            idea_id=payload.idea_id,
            parent_version_id=payload.version_id,
            instruction=payload.instruction,
            transformation_type=transformation,
        )

        new_active_version = ActiveIdeaVersion(
            version_id=new_version.id,
            idea_id=payload.idea_id,
            session_id=payload.session_id,
            title=new_version.content.title,
            content=new_version.content.description,
            status="active",
            version_number=new_version.version_number,
            parent_version_id=new_version.parent_version_id,
            source_variant_id=None,
            transformation_type=transformation.value,
        )

        return TransformVersionResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            previous_version_id=payload.version_id,
            new_active_version=new_active_version,
            message="Version transformed successfully",
        )

    # ── 5. COMPARE VERSIONS (AI via AnalysisService) ──────────────────────────

    async def compare_versions(
        self,
        payload: CompareVersionsRequest,
    ) -> CompareVersionsResponse:
        return await self._analysis_service.compare_versions(payload)

    # ── 6. EXPLORE PERSPECTIVE (AI via AnalysisService) ───────────────────────

    async def explore_perspective(
        self,
        payload: ExplorePerspectiveRequest,
    ) -> ExplorePerspectiveResponse:
        return await self._analysis_service.explore_perspective(payload)

    # ── 7. GENERATE FINAL SYNTHESIS (AI via SynthesisService) ─────────────────

    async def generate_final_synthesis(
        self,
        payload: GenerateFinalSynthesisRequest,
    ) -> GenerateFinalSynthesisResponse:
        return await self._synthesis_service.generate_final_synthesis(payload)
