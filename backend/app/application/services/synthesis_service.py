from __future__ import annotations

from app.application.dto.synthesis_dto import SynthesisResponse
from app.domain.repositories.synthesis_repository import SynthesisRepository
from app.domain.repositories.version_repository import VersionRepository
from app.infrastructure.ai.mappers.synthesis_mapper import map_synthesis_payload_to_entity
from app.infrastructure.ai.providers.mock_provider import MockAIProvider
from app.infrastructure.ai.providers.ollama_provider import OllamaProvider
from app.shared.errors.domain_errors import VersionNotFoundDomainError
from app.shared.utils.language import resolve_language
from app.shared.errors.domain_errors import IdeaNotFoundError, VersionNotFoundDomainError

class SynthesisService:
    def __init__(
        self,
        repository: SynthesisRepository,
        version_repository: VersionRepository,
        ai_provider: MockAIProvider | OllamaProvider,
    ) -> None:
        self.repository = repository
        self.version_repository = version_repository
        self.ai_provider = ai_provider

    def generate_synthesis(
        self,
        idea_id: str,
        version_id: str,
        preferred_language: str | None = "auto",
    ) -> SynthesisResponse:
        version = self.version_repository.get_by_id(version_id)
        if version is None:
            raise VersionNotFoundDomainError("Version not found.")

        if version.idea_id != idea_id:
            raise IdeaNotFoundError("Version does not belong to the provided idea.")

        language = resolve_language(
            preferred_language=preferred_language,
            fallback_text=version.content,
        )

        if isinstance(self.ai_provider, OllamaProvider):
            payload = self.ai_provider.generate_synthesis(
                idea_id=idea_id,
                version_id=version_id,
                version_content=version.content,
                language=language,
            )
        else:
            payload = self.ai_provider.generate_synthesis(
                idea_id=idea_id,
                version_id=version_id,
                language=language,
            )

        synthesis = map_synthesis_payload_to_entity(
            payload,
            idea_id=idea_id,
            version_id=version_id,
        )
        saved = self.repository.save(synthesis)

        return SynthesisResponse(
            id=saved.id,
            idea_id=saved.idea_id,
            version_id=saved.version_id,
            summary=saved.summary,
            value_proposition=saved.value_proposition,
            target_audience=saved.target_audience,
            structured_description=saved.structured_description,
            next_steps=saved.next_steps,
            created_at=saved.created_at,
        )