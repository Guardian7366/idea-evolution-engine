from __future__ import annotations

from app.application.dto.comparison_dto import ComparisonResponse
from app.application.dto.perspective_dto import PerspectiveResponse
from app.domain.repositories.analysis_repository import AnalysisRepository
from app.domain.repositories.version_repository import VersionRepository
from app.infrastructure.ai.mappers.analysis_mapper import map_analysis_payload_to_entity
from app.infrastructure.ai.mappers.comparison_mapper import map_comparison_payload_to_entity
from app.infrastructure.ai.providers.mock_provider import MockAIProvider
from app.infrastructure.ai.providers.ollama_provider import OllamaProvider
from app.shared.errors.domain_errors import VersionNotFoundDomainError
from app.shared.utils.language import resolve_language
from app.shared.errors.domain_errors import IdeaNotFoundError, VersionNotFoundDomainError

class AnalysisService:
    def __init__(
        self,
        repository: AnalysisRepository,
        version_repository: VersionRepository,
        ai_provider: MockAIProvider | OllamaProvider,
    ) -> None:
        self.repository = repository
        self.version_repository = version_repository
        self.ai_provider = ai_provider

    def analyze_perspective(
        self,
        version_id: str,
        perspective: str,
        preferred_language: str | None = "auto",
    ) -> PerspectiveResponse:
        version = self.version_repository.get_by_id(version_id)
        if version is None:
            raise VersionNotFoundDomainError("Version not found.")

        language = resolve_language(
            preferred_language=preferred_language,
            fallback_text=version.content,
        )

        if isinstance(self.ai_provider, OllamaProvider):
            payload = self.ai_provider.analyze_perspective(
                version_id=version_id,
                perspective=perspective,
                version_content=version.content,
                language=language,
            )
        else:
            payload = self.ai_provider.analyze_perspective(
                version_id=version_id,
                perspective=perspective,
                language=language,
            )

        analysis = map_analysis_payload_to_entity(payload, version_id=version_id)
        saved = self.repository.save_analysis(analysis)

        return PerspectiveResponse(
            id=saved.id,
            version_id=saved.version_id,
            analysis_type=saved.analysis_type,
            content=saved.content,
            created_at=saved.created_at,
        )

    def compare_versions(
        self,
        idea_id: str,
        left_version_id: str,
        right_version_id: str,
        preferred_language: str | None = "auto",
    ) -> ComparisonResponse:
        left_version = self.version_repository.get_by_id(left_version_id)
        if left_version is None:
            raise VersionNotFoundDomainError("Left version not found.")

        right_version = self.version_repository.get_by_id(right_version_id)
        if right_version is None:
            raise VersionNotFoundDomainError("Right version not found.")

        if left_version.idea_id != idea_id or right_version.idea_id != idea_id:
            raise IdeaNotFoundError("Versions do not belong to the provided idea.")

        if left_version.id == right_version.id:
            raise VersionNotFoundDomainError("Cannot compare a version with itself.")

        language = resolve_language(
            preferred_language=preferred_language,
            fallback_text=f"{left_version.content}\n{right_version.content}",
        )

        payload = self.ai_provider.compare_versions(
            left_version_content=left_version.content,
            right_version_content=right_version.content,
            language=language,
        )

        comparison = map_comparison_payload_to_entity(
            payload,
            idea_id=idea_id,
            left_version_id=left_version_id,
            right_version_id=right_version_id,
        )
        saved = self.repository.save_comparison(comparison)

        return ComparisonResponse(
            id=saved.id,
            idea_id=saved.idea_id,
            left_version_id=saved.left_version_id,
            right_version_id=saved.right_version_id,
            comparison_text=saved.comparison_text,
            created_at=saved.created_at,
        )