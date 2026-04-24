"""
analysis_service.py — Application service for version comparison and perspective analysis.

Owns all AI-powered analytical operations:
  - compare_versions: structural comparison of two idea versions
  - explore_perspective: single-lens analysis (feasibility, innovation, user_value, risks)

Receives OllamaProvider and VersionRepository via dependency injection.
"""

from app.application.dto.comparison_dto import (
    CompareVersionsRequest,
    CompareVersionsResponse,
)
from app.application.dto.perspective_dto import (
    ExplorePerspectiveRequest,
    ExplorePerspectiveResponse,
)
from app.domain.repositories.version_repository import VersionRepository
from app.infrastructure.ai.ollama_provider import OllamaProvider
from app.shared.database import db_wrapper


class AnalysisService:
    """
    Handles analytical operations over idea versions using the AI provider.
    """

    def __init__(
        self,
        version_repository: VersionRepository,
        ollama_provider: OllamaProvider,
    ) -> None:
        self._version_repo = version_repository
        self._provider = ollama_provider

    @db_wrapper
    async def compare_versions(
        self,
        payload: CompareVersionsRequest,
        **kwargs,
    ) -> CompareVersionsResponse:
        """
        Compare two idea versions using Ollama and return structured analysis.

        Fetches both versions from the repository to get their real content,
        then sends them to the AI provider for comparison.
        """
        # IMPORTANTE:
        # El backend también valida que no se compare una versión consigo misma.
        # No debemos depender solo del frontend para esta regla.
        if payload.version_id_a == payload.version_id_b:
            raise ValueError(
                "No se puede comparar una versión consigo misma. "
                "Selecciona dos versiones diferentes."
            )
        version_a = await self._version_repo.get_by_id(payload.version_id_a, kwargs["cursor"])
        if version_a is None or version_a.idea_id != payload.idea_id:
            raise ValueError(
                f"La versión '{payload.version_id_a}' no existe para la idea '{payload.idea_id}'."
            )

        version_b = await self._version_repo.get_by_id(payload.version_id_b, kwargs["cursor"])
        if version_b is None or version_b.idea_id != payload.idea_id:
            raise ValueError(
                f"La versión '{payload.version_id_b}' no existe para la idea '{payload.idea_id}'."
            )

        comparison = await self._provider.compare_versions(
            title_a=version_a.title,
            content_a=version_a.content,
            title_b=version_b.title,
            content_b=version_b.content,
        )

        return CompareVersionsResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            version_id_a=payload.version_id_a,
            version_id_b=payload.version_id_b,
            comparison=comparison,
            message="Versions compared successfully",
        )

    @db_wrapper
    async def explore_perspective(
        self,
        payload: ExplorePerspectiveRequest,
        **kwargs,
    ) -> ExplorePerspectiveResponse:
        """
        Analyze a specific idea version from the requested perspective using Ollama.
        """
        version = await self._version_repo.get_by_id(payload.version_id, kwargs["cursor"])
        if version is None or version.idea_id != payload.idea_id:
            raise ValueError(
                f"La versión '{payload.version_id}' no existe para la idea '{payload.idea_id}'."
            )

        analysis = await self._provider.explore_perspective(
            perspective_type=payload.perspective_type,
            title=version.title,
            content=version.content,
        )

        return ExplorePerspectiveResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            version_id=payload.version_id,
            analysis=analysis,
            message="Perspective explored successfully",
        )
