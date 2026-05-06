from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.application.dto.idea_dto import IdeaCreateRequest, IdeaResponse
from app.application.dto.variant_dto import VariantListResponse, VariantResponse
from app.domain.entities.idea import Idea
from app.domain.entities.idea_variant import IdeaVariant
from app.domain.repositories.idea_repository import IdeaRepository
from app.domain.repositories.session_repository import SessionRepository
from app.domain.value_objects.idea_content import IdeaContent
from app.infrastructure.ai.mappers.variant_mapper import map_variant_payloads_to_entities
from app.infrastructure.ai.providers.mock_provider import MockAIProvider
from app.infrastructure.ai.providers.ollama_provider import OllamaProvider
from app.shared.errors.domain_errors import IdeaNotFoundError, SessionNotFoundError
from app.shared.utils.language import resolve_language


class IdeaService:
    def __init__(
        self,
        idea_repository: IdeaRepository,
        session_repository: SessionRepository,
        ai_provider: MockAIProvider | OllamaProvider,
    ) -> None:
        self.idea_repository = idea_repository
        self.session_repository = session_repository
        self.ai_provider = ai_provider

    def create_idea(self, data: IdeaCreateRequest) -> IdeaResponse:
        session = self.session_repository.get_by_id(data.session_id)
        if session is None:
            raise SessionNotFoundError("Session not found.")

        now = datetime.now(timezone.utc)
        idea = Idea(
            id=f"idea_{uuid4().hex}",
            session_id=data.session_id,
            content=IdeaContent(data.content),
            title=data.title,
            created_at=now,
            updated_at=now,
        )
        saved = self.idea_repository.save_idea(idea)
        return self._to_idea_response(saved)

    def get_idea_by_id(self, idea_id: str) -> IdeaResponse | None:
        idea = self.idea_repository.get_idea_by_id(idea_id)
        if idea is None:
            return None
        return self._to_idea_response(idea)

    def generate_variants(
        self,
        idea_id: str,
        preferred_language: str | None = "auto",
    ) -> VariantListResponse:
        idea = self.idea_repository.get_idea_by_id(idea_id)
        if idea is None:
            raise IdeaNotFoundError("Idea not found.")

        existing_variants = self.idea_repository.list_variants_by_idea_id(idea_id)
        if existing_variants:
            return VariantListResponse(
                items=[self._to_variant_response(v) for v in existing_variants]
            )

        language = resolve_language(
            preferred_language=preferred_language,
            fallback_text=f"{idea.title or ''}\n{idea.content.value}",
        )

        payloads = self.ai_provider.generate_variants(
            idea.content.value,
            language=language,
        )
        variants = map_variant_payloads_to_entities(payloads, idea_id=idea_id)

        saved = self.idea_repository.save_variants(variants)
        return VariantListResponse(items=[self._to_variant_response(v) for v in saved])

    def list_variants_by_idea_id(self, idea_id: str) -> VariantListResponse:
        idea = self.idea_repository.get_idea_by_id(idea_id)
        if idea is None:
            raise IdeaNotFoundError("Idea not found.")

        variants = self.idea_repository.list_variants_by_idea_id(idea_id)
        return VariantListResponse(items=[self._to_variant_response(v) for v in variants])

    def _to_idea_response(self, idea: Idea) -> IdeaResponse:
        return IdeaResponse(
            id=idea.id,
            session_id=idea.session_id,
            content=idea.content.value,
            title=idea.title,
            created_at=idea.created_at,
            updated_at=idea.updated_at,
        )

    def _to_variant_response(self, variant: IdeaVariant) -> VariantResponse:
        return VariantResponse(
            id=variant.id,
            idea_id=variant.idea_id,
            title=variant.title,
            description=variant.description,
            order_index=variant.order_index,
            is_selected=variant.is_selected,
            selected_at=variant.selected_at,
            created_at=variant.created_at,
        )