"""
session_service.py — Servicio de aplicación para Sessions.

¿Qué hace este servicio?
Orquesta todas las operaciones sobre sesiones: crearlas, obtenerlas,
cambiar su estado y notificarles cuando se agregan ideas.

Es el intermediario entre la API y la entidad Session del dominio.
No contiene lógica de negocio propia — esa vive en Session y SessionRules.

CAMBIOS RESPECTO A SEMANA 1:
- Se eliminó register_new_version(): Session no tiene ese método.
  Las versiones no notifican a la sesión — se gestionan de forma independiente.
- Se corrigió get_all_sessions(): el repositorio define get_all(status=None),
  no get_all(limit, offset). Se eliminaron los parámetros de paginación
  que no existen en el contrato del repositorio.
- Se eliminó el parámetro user_id en create_session(): Session.create()
  solo acepta title.
- Se eliminó el parámetro content en create_session(): mismo motivo.
- SessionRules.can_be_completed() ahora lee directamente de session.idea_ids,
  no recibe total_ideas como parámetro externo.
"""
from sqlite3 import Cursor
from typing import Optional

from app.domain.entities.session import Session
from app.domain.repositories.session_repository import SessionRepository
from app.domain.rules.session_rules import SessionRules
from app.domain.value_objects.session_status import SessionStatus

# Título por defecto cuando el endpoint no recibe uno.
# Cuando sessions.py acepte título como parámetro, se deja de usar esta constante.
DEFAULT_SESSION_TITLE = "Nueva sesión"


class SessionService:
    """
    Servicio de aplicación para el ciclo de vida de Sessions.

    Recibe el repositorio por inyección de dependencias.
    No sabe si el repositorio habla con SQLite, un mock en memoria,
    o cualquier otra implementación — solo conoce la interfaz abstracta.
    """

    def __init__(self, session_repository: SessionRepository) -> None:
        # Repositorio abstracto. La implementación concreta se inyecta desde deps.py.
        self._repo = session_repository

    # ──────────────────────────────────────────────────────────────────────────
    # CREAR SESIÓN
    # ──────────────────────────────────────────────────────────────────────────

    async def create_session(self, title: Optional[str], cursor: Cursor) -> Session:
        """
        Crea una nueva sesión y la persiste.

        Parámetros:
        - title: Título de la sesión. Si no viene, se usa DEFAULT_SESSION_TITLE.
          Cuando sessions.py acepte título desde el frontend, solo se pasa aquí.

        Retorna: La entidad Session persistida con su ID real.

        NOTA: Se eliminaron los parámetros content y user_id porque
        Session.create() solo acepta title. Agregar campos a Session
        es decisión del equipo de dominio, no del servicio.
        """
        resolved_title = title.strip() if title and title.strip() else DEFAULT_SESSION_TITLE
        session = Session.create(title=resolved_title)
        return await self._repo.save(session, cursor)

    # ──────────────────────────────────────────────────────────────────────────
    # OBTENER SESIONES
    # ──────────────────────────────────────────────────────────────────────────

    async def get_session(self, session_id: str, cursor: Cursor) -> Session:
        """
        Retorna una sesión por su ID.
        Lanza ValueError si no existe — el endpoint lo convierte en HTTP 404.
        """
        session = await self._repo.get_by_id(session_id, cursor)
        if session is None:
            raise ValueError(
                f"Sesión '{session_id}' no encontrada. "
                "Verifica que el session_id sea correcto."
            )
        return session

    async def get_all_sessions(
        self, status: Optional[SessionStatus], cursor: Cursor
    ) -> list[Session]:
        """
        Retorna todas las sesiones, opcionalmente filtradas por estado.

        CORRECCIÓN SEMANA 2: La versión anterior llamaba get_all(limit, offset)
        pero SessionRepository define get_all(status=None). Se alineó la firma.
        La paginación puede agregarse al repositorio cuando se necesite,
        pero no debe asumirse antes de que exista.
        """
        return await self._repo.get_all(status=status, cursor=cursor)

    # ──────────────────────────────────────────────────────────────────────────
    # CAMBIOS DE ESTADO
    # ──────────────────────────────────────────────────────────────────────────

    async def pause_session(self, session_id: str, cursor: Cursor) -> Session:
        """
        Pausa una sesión activa.
        Si lanza error, la sesión no está en ACTIVE.
        El endpoint debe convertir ese error en HTTP 409 Conflict.
        """
        session = await self.get_session(session_id, cursor)
        session.pause()
        return await self._repo.save(session, cursor)

    async def resume_session(self, session_id: str, cursor: Cursor) -> Session:
        """
        Reanuda una sesión pausada.
        Solo funciona si está en PAUSED.
        """
        session = await self.get_session(session_id, cursor)
        session.resume()
        return await self._repo.save(session, cursor)

    async def complete_session(self, session_id: str, cursor: Cursor) -> Session:
        """
        Marca una sesión como completada.

        Valida con SessionRules.can_be_completed() que:
        1. La sesión está en ACTIVE.
        2. Tiene al menos una idea en session.idea_ids.

        Si falla por "sin ideas": idea_service no llamó register_idea_added()
        al crear ideas, o las ideas no se persistieron correctamente.
        """
        session = await self.get_session(session_id, cursor)
        # La rule lee directamente de session.idea_ids — no necesita parámetros extra.
        SessionRules.can_be_completed(session)
        session.complete()
        return await self._repo.save(session, cursor)

    async def archive_session(self, session_id: str, cursor: Cursor) -> Session:
        """
        Archiva una sesión. Puede archivarse desde PAUSED o COMPLETED.
        No puede archivarse una sesión ACTIVE directamente.
        """
        session = await self.get_session(session_id, cursor)
        session.archive()
        return await self._repo.save(session, cursor)

    # ──────────────────────────────────────────────────────────────────────────
    # SOPORTE PARA OTROS SERVICIOS
    # ──────────────────────────────────────────────────────────────────────────

    async def register_idea_added(self, session_id: str, idea_id: str, cursor: Cursor) -> Session:
        """
        Notifica a la sesión que se agregó una idea nueva.
        Delega a session.add_idea() que valida que la sesión esté activa
        y agrega el idea_id a session.idea_ids si no estaba ya.

        ¿Quién llama este método?
        idea_service.py después de persistir una idea exitosamente.

        Si lanza error: la sesión no está en ACTIVE. idea_service debe
        verificar el estado de la sesión ANTES de crear la idea.

        NOTA: Se eliminó register_version_added() porque Session no tiene
        ese método. Las versiones no notifican a la sesión — son entidades
        independientes gestionadas por VersionService.
        """
        session = await self.get_session(session_id, cursor)
        session.add_idea(idea_id)
        return await self._repo.save(session, cursor)

    async def assert_session_is_active(self, session_id: str, cursor: Cursor) -> Session:
        """
        Verifica que una sesión existe y está activa. Retorna la sesión.

        Método utilitario para que idea_service y version_service
        validen el estado antes de operar.

        Si lanza ValueError por "no encontrada" → HTTP 404 en el endpoint.
        Si lanza ValueError por "no editable"   → HTTP 409 en el endpoint.
        """
        session = await self.get_session(session_id, cursor)
        SessionRules.assert_is_editable(session)
        return session
