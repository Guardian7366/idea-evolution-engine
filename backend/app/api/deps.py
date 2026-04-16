"""
deps.py — FastAPI dependency providers.

Wires repositories, AI provider, and all application services together.
Only this file changes when swapping mock repos for real DB implementations.

Singletons created once at module load time so state persists across requests.
"""

from fastapi import Depends

from app.application.services.analysis_service import AnalysisService
from app.application.services.idea_service import IdeaService
from app.application.services.session_service import SessionService
from app.application.services.synthesis_service import SynthesisService
from app.application.services.version_service import VersionService
from app.infrastructure.ai.llm_client import get_llm_client
from app.infrastructure.ai.ollama_provider import OllamaProvider
from app.infrastructure.repositories.mock_idea_repository import MockIdeaRepository
from app.infrastructure.repositories.mock_session_repository import MockSessionRepository
from app.infrastructure.repositories.mock_version_repository import MockVersionRepository

# ── Repository singletons ─────────────────────────────────────────────────────
_mock_session_repo = MockSessionRepository()
_mock_idea_repo = MockIdeaRepository()
_mock_version_repo = MockVersionRepository()

# ── AI provider singleton ─────────────────────────────────────────────────────
_ollama_provider = OllamaProvider(get_llm_client())


# ── Service providers ─────────────────────────────────────────────────────────

def get_session_service() -> SessionService:
    return SessionService(_mock_session_repo)


def get_version_service() -> VersionService:
    return VersionService(_mock_version_repo, _mock_idea_repo, _ollama_provider)


def get_analysis_service() -> AnalysisService:
    return AnalysisService(_mock_version_repo, _ollama_provider)


def get_synthesis_service() -> SynthesisService:
    return SynthesisService(_mock_idea_repo, _mock_version_repo, _ollama_provider)


def get_idea_service(
    session_service: SessionService = Depends(get_session_service),
    version_service: VersionService = Depends(get_version_service),
    analysis_service: AnalysisService = Depends(get_analysis_service),
    synthesis_service: SynthesisService = Depends(get_synthesis_service),
) -> IdeaService:
    return IdeaService(
        _mock_idea_repo,
        session_service,
        version_service,
        _ollama_provider,
        analysis_service,
        synthesis_service,
    )
