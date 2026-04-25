"""
synthesis_service.py — Application service for generating the final idea synthesis.

Owns the AI-powered synthesis operation:
  - generate_final_synthesis: produces a structured summary of the evolved idea

Receives OllamaProvider, IdeaRepository and VersionRepository via dependency injection.
"""
from sqlite3 import Cursor

from app.application.dto.synthesis_dto import (
    GenerateFinalSynthesisRequest,
    GenerateFinalSynthesisResponse,
)
from app.domain.repositories.idea_repository import IdeaRepository
from app.domain.repositories.version_repository import VersionRepository
from app.infrastructure.ai.ollama_provider import OllamaProvider


class SynthesisService:
    """
    Generates the final structured synthesis of an evolved idea using the AI provider.
    """

    def __init__(
        self,
        idea_repository: IdeaRepository,
        version_repository: VersionRepository,
        ollama_provider: OllamaProvider,
    ) -> None:
        self._idea_repo = idea_repository
        self._version_repo = version_repository
        self._provider = ollama_provider

    async def generate_final_synthesis(
        self,
        payload: GenerateFinalSynthesisRequest,
        cursor: Cursor,
    ) -> GenerateFinalSynthesisResponse:
        """
        Generate the final synthesis for an idea in its current version state.

        Fetches the idea (for the original prompt) and the target version (for
        final content), counts the total versions for context, then calls the
        AI provider for synthesis.
        """
        idea = await self._idea_repo.get_by_id(payload.idea_id, cursor)
        if idea is None:
            raise ValueError(f"La idea '{payload.idea_id}' no existe.")

        version = await self._version_repo.get_by_id(payload.version_id, cursor)
        if version is None or version.idea_id != payload.idea_id:
            raise ValueError(
                f"La versión '{payload.version_id}' no existe para la idea '{payload.idea_id}'."
            )

        all_versions = await self._version_repo.get_by_idea_id(payload.idea_id, cursor)
        total_versions = len(all_versions)

        synthesis = await self._provider.generate_synthesis(
            original_prompt=idea.content,
            final_title=version.title,
            final_content=version.content,
            total_versions=total_versions,
        )

        return GenerateFinalSynthesisResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            version_id=payload.version_id,
            synthesis=synthesis,
            message="Final synthesis generated successfully",
        )
