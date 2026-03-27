"""
mock_session_repository.py — Implementación en memoria de SessionRepository.

¿Por qué existe este archivo?
- El dominio define SessionRepository como interfaz abstracta (ABC).
- La infraestructura real (SQLAlchemy, etc.) aún no está implementada.
- Este mock permite que SessionService funcione completamente hoy,
  sin depender de que la BD esté lista.

¿Dónde vive este archivo en el proyecto?
- Opción A (recomendada para ahora): infrastructure/repositories/mock_session_repository.py
- Opción B: tests/mocks/ si el equipo prefiere mantenerlo solo para testing.

¿Cuándo se reemplaza?
- Cuando infrastructure/repositories/session_repository_impl.py esté implementado,
  solo se cambia la línea en deps.py que instancia el repositorio.
  SessionService no necesita ningún cambio.

Limitación importante:
- Los datos solo persisten mientras el servidor está corriendo.
- Cada reinicio del servidor borra todas las sesiones.
- Esto es esperado para Semana 1.
"""

from typing import Dict, List, Optional

from app.domain.entities.session import Session
from app.domain.repositories.session_repository import SessionRepository
from app.domain.value_objects.session_status import SessionStatus


class MockSessionRepository(SessionRepository):
    """
    Repositorio de sesiones en memoria.
    Implementa todos los métodos abstractos de SessionRepository usando un dict.

    El dict _store usa session.id como clave y la entidad Session como valor.
    """

    def __init__(self) -> None:
        # Diccionario en memoria: { session_id: Session }
        # Es el único "storage" de este mock.
        self._store: Dict[str, Session] = {}

    async def save(self, session: Session) -> Session:
        """
        Guarda o actualiza una sesión en memoria.
        Retorna la misma sesión recibida (sin transformaciones).

        En la implementación real con SQLAlchemy, aquí se haría
        db.add(model) y await db.commit(). La interfaz no cambia.
        """
        self._store[session.id] = session
        return session

    async def get_by_id(self, session_id: str) -> Optional[Session]:
        """
        Retorna la sesión con ese ID o None si no existe.
        El servicio es responsable de lanzar error si el resultado es None.
        """
        return self._store.get(session_id)

    async def get_all(self, limit: int = 50, offset: int = 0) -> List[Session]:
        """
        Retorna todas las sesiones paginadas, ordenadas por created_at descendente
        (más recientes primero).

        En la implementación real, esto sería una query con ORDER BY y LIMIT/OFFSET.
        """
        all_sessions = sorted(
            self._store.values(),
            key=lambda s: s.created_at,
            reverse=True,
        )
        return all_sessions[offset: offset + limit]

    async def get_by_status(self, status: SessionStatus) -> List[Session]:
        """Retorna todas las sesiones con un estado específico."""
        return [s for s in self._store.values() if s.status == status]

    async def delete(self, session_id: str) -> bool:
        """
        Elimina una sesión del store.
        Retorna True si existía y fue eliminada, False si no existía.
        """
        if session_id in self._store:
            del self._store[session_id]
            return True
        return False

    async def exists(self, session_id: str) -> bool:
        """Verifica si una sesión existe sin cargarla completa."""
        return session_id in self._store