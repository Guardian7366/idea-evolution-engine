"""
deps.py — FastAPI dependency providers.

Wires repositories, AI provider, and all application services together.
Only this file changes when swapping mock repos for real DB implementations.

Singletons created once at module load time so state persists across requests.
"""

import sqlite3
from app.shared.config import settings
from fastapi import Depends
from app.application.services.analysis_service import AnalysisService
from app.application.services.idea_service import IdeaService
from app.application.services.session_service import SessionService
from app.application.services.synthesis_service import SynthesisService
from app.application.services.version_service import VersionService
from app.infrastructure.ai.llm_client import get_llm_client
from app.infrastructure.ai.ollama_provider import OllamaProvider
from app.infrastructure.repositories.idea_repository_impl import IdeaRepository
from app.infrastructure.repositories.session_repository_impl import SessionRepository
from app.infrastructure.repositories.version_repository_impl import VersionRepository

# ── Repository singletons ─────────────────────────────────────────────────────

_session_repo = SessionRepository()
_idea_repo = IdeaRepository()
_version_repo = VersionRepository()

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

def get_db_cursor():
    conn = sqlite3.connect(settings.database_name, check_same_thread=False)
    try:
        yield conn.cursor()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
