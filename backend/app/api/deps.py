"""
deps.py — Proveedores de dependencias para FastAPI.

Este archivo conecta los servicios con los endpoints.
Cada función get_X_service() le dice a FastAPI cómo construir ese servicio
cuando un endpoint lo pide con Depends().

Estado actual: todos los servicios usan repositorios mock en memoria.
Cuando la BD real esté lista, solo se cambian las líneas que instancian
los repositorios — los servicios y endpoints no necesitan cambios.

IMPORTANTE: Los objetos _mock_X_repo se crean UNA SOLA VEZ fuera de las funciones.
Si se crearan dentro de cada función, cada request tendría su propio repositorio
vacío y los datos no persistirían entre llamadas.
"""

from fastapi import Depends

from app.application.services.session_service import SessionService
from app.application.services.version_service import VersionService
from app.application.services.idea_service import IdeaService
from app.infrastructure.repositories.mock_session_repository import MockSessionRepository
from app.infrastructure.repositories.mock_idea_repository import MockIdeaRepository
from app.infrastructure.repositories.mock_version_repository import MockVersionRepository

# ── Singletons de repositorios mock ──────────────────────────────────────────
# Instancias únicas compartidas entre todos los requests mientras el servidor corre.
# Se pierden al reiniciar el servidor (comportamiento esperado en Semana 1).

_mock_session_repo = MockSessionRepository()
_mock_idea_repo = MockIdeaRepository()
_mock_version_repo = MockVersionRepository()


# ── Proveedores de servicios ──────────────────────────────────────────────────

def get_session_service() -> SessionService:
    """
    Proveedor de SessionService.
    Uso en endpoints: service: SessionService = Depends(get_session_service)
    """
    return SessionService(_mock_session_repo)


def get_version_service() -> VersionService:
    """
    Proveedor de VersionService.
    Recibe VersionRepository e IdeaRepository porque necesita ambos:
    - VersionRepository para persistir versiones.
    - IdeaRepository para verificar que la idea padre existe.

    Uso en endpoints: service: VersionService = Depends(get_version_service)
    """
    return VersionService(_mock_version_repo, _mock_idea_repo)


def get_idea_service(
    session_service: SessionService = Depends(get_session_service),
    version_service: VersionService = Depends(get_version_service),
) -> IdeaService:
    """
    Proveedor de IdeaService.
    Recibe SessionService y VersionService porque los necesita para orquestar el flujo.
    FastAPI los inyecta automáticamente encadenando los proveedores de arriba.

    Uso en endpoints: service: IdeaService = Depends(get_idea_service)
    """
    return IdeaService(_mock_idea_repo, session_service, version_service)