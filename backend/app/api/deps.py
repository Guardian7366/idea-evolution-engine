from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session as DBSession

from app.application.services.analysis_service import AnalysisService
from app.application.services.idea_service import IdeaService
from app.application.services.session_service import SessionService
from app.application.services.synthesis_service import SynthesisService
from app.application.services.version_service import VersionService
from app.infrastructure.ai.clients.llm_client import LLMClient
from app.infrastructure.ai.providers.mock_provider import MockAIProvider
from app.infrastructure.ai.providers.ollama_provider import OllamaProvider
from app.infrastructure.persistence.database import get_db
from app.infrastructure.repositories.analysis_repository_impl import SqliteAnalysisRepository
from app.infrastructure.repositories.idea_repository_impl import SqliteIdeaRepository
from app.infrastructure.repositories.session_repository_impl import SqliteSessionRepository
from app.infrastructure.repositories.synthesis_repository_impl import SqliteSynthesisRepository
from app.infrastructure.repositories.version_repository_impl import SqliteVersionRepository
from app.shared.config import settings
from app.shared.errors.infrastructure_errors import AIProviderConfigurationError


def get_settings():
    return settings


def get_ai_provider():
    provider_name = settings.llm_provider.strip().lower()

    if provider_name == "mock":
        return MockAIProvider()

    if provider_name == "ollama":
        client = LLMClient(base_url=settings.ollama_base_url)
        return OllamaProvider(
            client=client,
            default_model=settings.ollama_model_default,
            spanish_model=settings.ollama_model_es,
            english_model=settings.ollama_model_en,
        )

    raise AIProviderConfigurationError(
        f"Unsupported LLM_PROVIDER value: {settings.llm_provider}"
    )


def get_session_service(
    db: DBSession = Depends(get_db),
) -> SessionService:
    session_repository = SqliteSessionRepository(db)
    return SessionService(session_repository)


def get_idea_service(
    db: DBSession = Depends(get_db),
    ai_provider = Depends(get_ai_provider),
) -> IdeaService:
    idea_repository = SqliteIdeaRepository(db)
    session_repository = SqliteSessionRepository(db)
    return IdeaService(idea_repository, session_repository, ai_provider)


def get_version_service(
    db: DBSession = Depends(get_db),
    ai_provider = Depends(get_ai_provider),
) -> VersionService:
    version_repository = SqliteVersionRepository(db)
    idea_repository = SqliteIdeaRepository(db)
    return VersionService(version_repository, idea_repository, ai_provider)


def get_analysis_service(
    db: DBSession = Depends(get_db),
    ai_provider = Depends(get_ai_provider),
) -> AnalysisService:
    repository = SqliteAnalysisRepository(db)
    version_repository = SqliteVersionRepository(db)
    return AnalysisService(repository, version_repository, ai_provider)


def get_synthesis_service(
    db: DBSession = Depends(get_db),
    ai_provider = Depends(get_ai_provider),
) -> SynthesisService:
    repository = SqliteSynthesisRepository(db)
    version_repository = SqliteVersionRepository(db)
    return SynthesisService(repository, version_repository, ai_provider)