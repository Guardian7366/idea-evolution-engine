"""
deps.py — Fragmento relevante para SessionService.

Este fragmento debe agregarse a tu archivo deps.py existente.
No reemplaces el archivo completo, solo añade estas líneas.

¿Qué hace get_session_service?
- Es la función de inyección de dependencias de FastAPI.
- Cada vez que un endpoint declara service: SessionService = Depends(get_session_service),
  FastAPI llama esta función y pasa el resultado al endpoint.
- Hoy retorna SessionService con el mock en memoria.
- Cuando exista la BD real, solo se cambia MockSessionRepository
  por SessionRepositoryImpl(db) aquí, sin tocar el servicio ni los endpoints.

Nota sobre el singleton del mock:
- _mock_session_repo se instancia una sola vez al arrancar el servidor.
- Esto garantiza que todos los endpoints compartan el mismo "storage" en memoria.
- Si se instanciara dentro de get_session_service(), cada request tendría
  su propio store vacío y las sesiones no persistirían entre llamadas.
"""

from app.application.services.session_service import SessionService
from app.infrastructure.repositories.mock_session_repository import MockSessionRepository
from app.application.services.version_service import VersionService
from app.infrastructure.repositories.mock_version_repository import MockVersionRepository
from app.infrastructure.repositories.mock_idea_repository import MockIdeaRepository

# Instancia única del mock compartida entre todos los requests.
# Reemplazar por la implementación real cuando esté lista.
_mock_session_repo = MockSessionRepository()

# Singletons compartidos entre todos los requests.
_mock_version_repo = MockVersionRepository()
_mock_idea_repo = MockIdeaRepository()
 


def get_session_service() -> SessionService:
    """
    Proveedor de SessionService para inyección de dependencias en FastAPI.

    Uso en endpoints:
        @router.post("")
        async def create_session(
            service: SessionService = Depends(get_session_service),
        ): ...

    Cuando se implemente la BD real, este método quedará así:
        def get_session_service(db: AsyncSession = Depends(get_db)) -> SessionService:
            return SessionService(SessionRepositoryImpl(db))
    """
    return SessionService(_mock_session_repo)

def get_version_service() -> VersionService:
    """
    Proveedor de VersionService para inyección de dependencias en FastAPI.
 
    Uso en endpoints:
        @router.post("/transform-version")
        async def transform_version(
            service: VersionService = Depends(get_version_service),
        ): ...
 
    Cuando la BD real esté lista:
        def get_version_service(db: AsyncSession = Depends(get_db)) -> VersionService:
            return VersionService(
                VersionRepositoryImpl(db),
                IdeaRepositoryImpl(db),
            )
    """
    return VersionService(_mock_version_repo, _mock_idea_repo)
 
