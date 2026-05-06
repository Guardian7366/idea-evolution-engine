from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.application.dto.selection_dto import VariantSelectionRequest
from app.application.dto.transformation_dto import TransformVersionRequest
from app.application.dto.version_dto import VersionListResponse, VersionResponse
from app.domain.entities.idea_version import IdeaVersion
from app.domain.repositories.idea_repository import IdeaRepository
from app.domain.repositories.version_repository import VersionRepository
from app.domain.rules.version_rules import ensure_variant_can_be_selected
from app.domain.value_objects.transformation_type import TransformationType
from app.domain.value_objects.version_status import VersionStatus
from app.infrastructure.ai.mappers.transformation_mapper import (
    map_transformation_payload_to_entity,
)
from app.infrastructure.ai.providers.mock_provider import MockAIProvider
from app.infrastructure.ai.providers.ollama_provider import OllamaProvider
from app.shared.errors.domain_errors import (
    IdeaNotFoundError,
    InvalidTransformationDomainError,
    VariantNotFoundError,
    VariantSelectionError,
    VersionNotFoundDomainError,
)
from app.shared.utils.language import resolve_language


class VersionService:
    def __init__(
        self,
        version_repository: VersionRepository,
        idea_repository: IdeaRepository,
        ai_provider: MockAIProvider | OllamaProvider,
    ) -> None:
        self.version_repository = version_repository
        self.idea_repository = idea_repository
        self.ai_provider = ai_provider

    def create_initial_version_from_variant(
        self,
        data: VariantSelectionRequest,
    ) -> VersionResponse:
        idea = self.idea_repository.get_idea_by_id(data.idea_id)
        if idea is None:
            raise IdeaNotFoundError("Idea not found.")

        variant = self.idea_repository.get_variant_by_id(data.variant_id)
        if variant is None:
            raise VariantNotFoundError("Variant not found.")

        if variant.idea_id != data.idea_id:
            raise VariantSelectionError("Variant does not belong to the provided idea.")

        ensure_variant_can_be_selected(variant)

        self.idea_repository.mark_variant_selected(data.variant_id)
        self.version_repository.deactivate_active_versions(data.idea_id)

        existing_versions = self.version_repository.list_by_idea_id(data.idea_id)
        next_version_number = len(existing_versions) + 1

        now = datetime.now(timezone.utc)

        language = resolve_language(
            preferred_language=data.language,
            fallback_text=f"{idea.title or ''}\n{idea.content.value}\n{variant.title}\n{variant.description}",
        )

        version = IdeaVersion(
            id=f"ver_{uuid4().hex}",
            idea_id=data.idea_id,
            content=self._build_initial_version_content(
                variant_title=variant.title,
                variant_description=variant.description,
                language=language,
            ),
            version_number=next_version_number,
            transformation_type=TransformationType.VARIANT_SELECTION,
            source_variant_id=data.variant_id,
            is_active=True,
            status=VersionStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )
        saved = self.version_repository.save(version)
        return self._to_response(saved)

    def transform_version(self, data: TransformVersionRequest) -> VersionResponse:
        parent_version = self.version_repository.get_by_id(data.version_id)
        if parent_version is None:
            raise VersionNotFoundDomainError("Version not found.")

        idea = self.idea_repository.get_idea_by_id(parent_version.idea_id)
        if idea is None:
            raise IdeaNotFoundError("Idea not found.")

        transformation_type = self._parse_transformation_type(data.transformation_type)

        if transformation_type == TransformationType.REFINEMENT and not data.instruction:
            raise InvalidTransformationDomainError(
                "Refinement requires a user instruction."
            )

        self.version_repository.deactivate_active_versions(parent_version.idea_id)

        existing_versions = self.version_repository.list_by_idea_id(parent_version.idea_id)
        next_version_number = len(existing_versions) + 1

        language = resolve_language(
            preferred_language=data.language,
            fallback_text=f"{data.instruction or ''}\n{parent_version.content}",
        )

        payload = self.ai_provider.transform_version(
            parent_content=parent_version.content,
            transformation_type=transformation_type,
            instruction=data.instruction,
            language=language,
        )

        new_version = map_transformation_payload_to_entity(
            payload,
            idea_id=parent_version.idea_id,
            version_number=next_version_number,
            parent_version_id=parent_version.id,
            transformation_type=transformation_type,
            user_instruction=data.instruction,
        )

        saved = self.version_repository.save(new_version)
        return self._to_response(saved)

    def activate_version(self, version_id: str) -> VersionResponse:
        version = self.version_repository.get_by_id(version_id)
        if version is None:
            raise VersionNotFoundDomainError("Version not found.")

        idea = self.idea_repository.get_idea_by_id(version.idea_id)
        if idea is None:
            raise IdeaNotFoundError("Idea not found.")

        self.version_repository.deactivate_active_versions(version.idea_id)
        activated = self.version_repository.activate_version(version.id)

        if activated is None:
            raise VersionNotFoundDomainError("Version not found.")

        return self._to_response(activated)

    def list_versions_by_idea_id(self, idea_id: str) -> VersionListResponse:
        idea = self.idea_repository.get_idea_by_id(idea_id)
        if idea is None:
            raise IdeaNotFoundError("Idea not found.")

        versions = self.version_repository.list_by_idea_id(idea_id)
        return VersionListResponse(items=[self._to_response(v) for v in versions])

    def _parse_transformation_type(self, value: str) -> TransformationType:
        normalized = value.strip().lower()

        mapping = {
            "evolution": TransformationType.EVOLUTION,
            "refinement": TransformationType.REFINEMENT,
            "mutation": TransformationType.MUTATION,
        }

        if normalized not in mapping:
            raise InvalidTransformationDomainError(
                "Invalid transformation_type. Use evolution, refinement or mutation."
            )

        return mapping[normalized]

    def _to_response(self, version: IdeaVersion) -> VersionResponse:
        return VersionResponse(
            id=version.id,
            idea_id=version.idea_id,
            content=version.content,
            version_number=version.version_number,
            transformation_type=version.transformation_type.value,
            source_variant_id=version.source_variant_id,
            parent_version_id=version.parent_version_id,
            user_instruction=version.user_instruction,
            is_active=version.is_active,
            status=version.status.value,
            created_at=version.created_at,
            updated_at=version.updated_at,
        )

    def _build_initial_version_content(
        self,
        *,
        variant_title: str,
        variant_description: str,
        language: str,
    ) -> str:
        if language == "es":
            return (
                f"Versión inicial creada a partir de la variante: "
                f"{variant_title}. {variant_description}"
            )

        return (
            f"Initial version created from variant: "
            f"{variant_title}. {variant_description}"
        )