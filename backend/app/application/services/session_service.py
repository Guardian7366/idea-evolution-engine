"""
session_service.py — Servicio de aplicación para Sessions.

¿Qué es un servicio de aplicación?
- Es el orquestador entre la API y el dominio.
- Recibe datos simples (strings, IDs), llama a las entidades, aplica las rules,
  usa los repositorios, y retorna resultados listos para la API.
- NO contiene lógica de negocio propia: esa vive en domain/entities/ y domain/rules/.
- NO sabe nada de HTTP, FastAPI ni Pydantic. Solo trabaja con entidades del dominio.

Flujo general de cualquier método en este servicio:
  1. Validar con Rules (¿está permitida esta operación?)
  2. Obtener/crear entidades del dominio
  3. Ejecutar la operación sobre la entidad
  4. Persistir cambios via repositorio
  5. Retornar el resultado

¿Por qué async?
- Los repositorios son async (definidos así en domain/repositories/).
- Cuando la infraestructura implemente SQLAlchemy async o cualquier ORM async,
  este servicio ya estará listo sin necesidad de refactor.
- El endpoint actual es sync (def), pero puede llamar métodos async usando
  asyncio.run() o convirtiendo el endpoint a async def cuando sea necesario.
"""

from typing import Optional

from app.domain.entities.session import Session
from app.domain.repositories.session_repository import SessionRepository
from app.domain.rules.session_rules import SessionRules
from app.domain.value_objects.session_status import SessionStatus

# Título que se usa cuando el endpoint no recibe uno explícito.
# Cuando el equipo actualice sessions.py para aceptar título como parámetro,
# simplemente se deja de usar esta constante y se pasa el valor recibido.
DEFAULT_SESSION_TITLE = "Nueva sesión"


class SessionService:
    """
    Servicio de aplicación para el ciclo de vida de Sessions.

    Recibe el repositorio por inyección de dependencias (parámetro del constructor).
    Esto significa que este servicio no sabe si el repositorio habla con una BD real,
    un mock en memoria, o cualquier otra implementación — solo conoce la interfaz.

    ¿Cómo se inyecta en FastAPI?
    En deps.py se creará una función get_session_service() que instancia este
    servicio con la implementación real o mock del repositorio según el entorno.
    Ejemplo futuro en deps.py:
        def get_session_service() -> SessionService:
            repo = SessionRepositoryImpl(db)  # implementación real
            return SessionService(repo)
    """

    def __init__(self, session_repository: SessionRepository) -> None:
        # Guardamos el repositorio como atributo privado.
        # Usamos el tipo abstracto (SessionRepository), no la implementación concreta.
        # Esto permite swappear el repositorio en tests sin tocar este servicio.
        self._repo = session_repository

    # ──────────────────────────────────────────────────────────────────────────
    # CREAR SESIÓN
    # ──────────────────────────────────────────────────────────────────────────

    async def create_session(
        self,
        title: Optional[str] = None,
        content: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> Session:
        """
        Crea una nueva sesión y la persiste.

        Parámetros:
        - title: Título de la sesión. Si no se recibe (como en el endpoint actual),
          se usa DEFAULT_SESSION_TITLE ("Nueva sesión").
          Cuando sessions.py acepte título como parámetro de entrada,
          simplemente pásalo aquí y la lógica no cambia.
        - content: Contenido opcional. Por ahora el endpoint no lo envía tampoco.
        - user_id: Preparado para autenticación futura. Por ahora siempre None.

        Retorna: La entidad Session ya persistida (con ID real asignado).

        ¿Por qué no retorna SessionCreateResponse directamente?
        Porque el servicio no conoce los DTOs de la API. El endpoint en sessions.py
        es responsable de mapear Session → SessionCreateResponse.
        """
        # Usamos el título recibido, o el default si no viene ninguno.
        # strip() para evitar títulos con solo espacios en blanco.
        resolved_title = (title.strip() if title and title.strip() else DEFAULT_SESSION_TITLE)

        # Session.create() es el factory method de la entidad.
        # Genera UUID, timestamps y nace en estado ACTIVE automáticamente.
        session = Session.create(
            title=resolved_title,
        )

        # Persistimos la sesión via repositorio abstracto.
        # En este momento el repositorio es un mock (retorna la misma entidad).
        # Cuando se implemente la BD real en infrastructure/repositories/,
        # este código no cambia — solo cambia la implementación del repositorio.
        persisted = await self._repo.save(session)

        return persisted

    # ──────────────────────────────────────────────────────────────────────────
    # OBTENER SESIÓN
    # ──────────────────────────────────────────────────────────────────────────

    async def get_session(self, session_id: str) -> Session:
        """
        Retorna una sesión por su ID.

        Lanza ValueError si la sesión no existe.
        El endpoint convierte este ValueError en un HTTP 404.

        ¿Por qué ValueError y no una excepción custom?
        Por ahora es suficiente. Cuando se implementen los errores de dominio
        en shared/errors/domain_errors.py, este método puede lanzar
        SessionNotFoundError en su lugar sin romper el contrato del endpoint.
        """
        session = await self._repo.get_by_id(session_id)

        if session is None:
            # Mensaje descriptivo para que el endpoint pueda mostrarlo al usuario
            # o para que aparezca claro en los logs.
            raise ValueError(
                f"Sesión con ID '{session_id}' no encontrada. "
                "Verifica que el session_id sea correcto y que la sesión no haya sido eliminada."
            )

        return session

    async def get_all_sessions(self, limit: int = 50, offset: int = 0) -> list[Session]:
        """
        Retorna todas las sesiones paginadas.

        Parámetros:
        - limit: Máximo de resultados por página. Default 50.
        - offset: Desde qué posición empezar. Default 0 (primera página).

        Cuando el endpoint de listado se implemente en sessions.py,
        estos parámetros vendrán como query params (?limit=20&offset=0).
        """
        return await self._repo.get_all(limit=limit, offset=offset)

    # ──────────────────────────────────────────────────────────────────────────
    # CAMBIOS DE ESTADO
    # ──────────────────────────────────────────────────────────────────────────

    async def pause_session(self, session_id: str) -> Session:
        """
        Pausa una sesión activa.

        Flujo:
        1. Obtiene la sesión (lanza ValueError si no existe).
        2. Llama session.pause() que internamente valida la transición de estado.
        3. Persiste el cambio.

        Si pause() lanza ValueError, significa que la sesión no está en ACTIVE.
        El endpoint debe convertir ese error en HTTP 409 Conflict.
        """
        session = await self.get_session(session_id)

        # pause() vive en la entidad Session y delega a transition_to(),
        # que usa SessionStatus.can_transition_to() para validar.
        # Si esto falla, el estado actual no permite pausa (ej: ya está ARCHIVED).
        session.pause()

        return await self._repo.save(session)

    async def resume_session(self, session_id: str) -> Session:
        """
        Reanuda una sesión pausada.

        Solo funciona si la sesión está en PAUSED.
        Si lanza error, revisa el estado actual de la sesión antes de llamar este método.
        """
        session = await self.get_session(session_id)
        session.resume()
        return await self._repo.save(session)

    async def complete_session(self, session_id: str) -> Session:
        """
        Marca una sesión como completada.

        Usa SessionRules.assert_can_be_completed() que valida:
        1. La sesión debe estar en ACTIVE.
        2. Debe tener al menos 1 idea registrada.

        Si falla con "sesión sin ideas", el contador total_ideas de la entidad
        es 0. Esto puede pasar si register_new_idea() nunca fue llamado por
        idea_service al crear ideas. Revisa idea_service.py cuando esté implementado.
        """
        session = await self.get_session(session_id)

        # IMPORTANTE:
        # La regla ahora toma la verdad directamente desde session.idea_ids.
        SessionRules.can_be_completed(session)

        session.complete()
        return await self._repo.save(session)

    async def archive_session(self, session_id: str) -> Session:
        """
        Archiva una sesión.

        Puede archivarse desde PAUSED o COMPLETED (ver SessionStatus.can_transition_to).
        No puede archivarse una sesión ACTIVE directamente — primero debe pausarse o completarse.
        """
        session = await self.get_session(session_id)
        session.archive()
        return await self._repo.save(session)

    # ──────────────────────────────────────────────────────────────────────────
    # OPERACIONES DE SOPORTE (usadas por otros servicios)
    # ──────────────────────────────────────────────────────────────────────────

    async def register_idea_added(self, session_id: str, idea_id: str) -> Session:
        """
        Notifica a la sesión que se agregó una nueva idea.
        Incrementa el contador total_ideas y valida que la sesión sea editable.

        ¿Quién llama este método?
        idea_service.py cuando crea una idea exitosamente.
        Esto mantiene sincronizado el contador de la sesión sin queries adicionales.

        Si lanza error aquí, la sesión no está en ACTIVE.
        idea_service.py debe verificar el estado de la sesión ANTES de crear la idea.
        """
        session = await self.get_session(session_id)

        # add_idea() valida internamente que la sesión sea editable.
        # Si lanza error, es porque la sesión no está en ACTIVE.
        session.add_idea(idea_id)

        return await self._repo.save(session)

    async def register_version_added(self, session_id: str) -> Session:
        """
        Notifica a la sesión que se creó una nueva versión.
        Incrementa el contador total_versions.

        ¿Quién llama este método?
        version_service.py cuando crea una versión exitosamente.
        """
        session = await self.get_session(session_id)
        session.register_new_version()
        return await self._repo.save(session)

    async def assert_session_is_active(self, session_id: str) -> Session:
        """
        Verifica que una sesión existe y está activa. Retorna la sesión.

        Método utilitario para que otros servicios (idea_service, version_service)
        validen el estado de la sesión antes de operar sobre sus ideas o versiones.

        Uso esperado en idea_service.py:
            session = await self._session_service.assert_session_is_active(session_id)
            # Si llega aquí, la sesión existe y está ACTIVE.
            idea = Idea.create(session_id=session.id, ...)

        Si lanza ValueError por sesión no encontrada → HTTP 404 en el endpoint.
        Si lanza ValueError por sesión no editable → HTTP 409 en el endpoint.
        """
        session = await self.get_session(session_id)
        SessionRules.assert_is_editable(session)
        return session
