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

# IMPORTANTE:
# Esta sección permite cambiar fácilmente entre mock y DB real en Semana 2+
# Sin tocar el resto del sistema.

USE_MOCK_REPOS = True  # ⚠️ Backend 1 cambiará esto en el futuro

if USE_MOCK_REPOS:
    _session_repo = MockSessionRepository()
    _idea_repo = MockIdeaRepository()
    _version_repo = MockVersionRepository()
else:
    # Placeholder para repositorios reales (SQLite)
    # Backend 1 / Backend 2 implementarán esto
    raise NotImplementedError("Repositorios reales aún no implementados")

# ── AI provider singleton ─────────────────────────────────────────────────────
_ollama_provider = OllamaProvider(get_llm_client())


# ── Service providers ─────────────────────────────────────────────────────────

def get_session_service() -> SessionService:
    return SessionService(_session_repo)


def get_version_service() -> VersionService:
    return VersionService(_version_repo, _idea_repo, _ollama_provider)


def get_analysis_service() -> AnalysisService:
    return AnalysisService(_version_repo, _ollama_provider)


def get_synthesis_service() -> SynthesisService:
    return SynthesisService(_idea_repo, _version_repo, _ollama_provider)


def get_idea_service(
    session_service: SessionService = Depends(get_session_service),
    version_service: VersionService = Depends(get_version_service),
    analysis_service: AnalysisService = Depends(get_analysis_service),
    synthesis_service: SynthesisService = Depends(get_synthesis_service),
) -> IdeaService:
    return IdeaService(
        _idea_repo,
        session_service,
        version_service,
        _ollama_provider,
        analysis_service,
        synthesis_service,
    )
