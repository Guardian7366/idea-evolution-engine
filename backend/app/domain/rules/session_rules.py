from app.domain.entities.session import Session
from app.domain.value_objects.session_status import SessionStatus


class SessionRules:
    """
    Reglas de negocio puras para el ciclo de vida de una Session.

    ¿Por qué una clase de rules separada y no poner esto en la entidad?
    Las entidades conocen su propio estado (ej: "puedo transicionar a X").
    Las rules conocen el contexto más amplio (ej: "¿tiene ideas? ¿hay versiones abiertas?").
    Separar esto evita que Session.py crezca indefinidamente y mezcle
    responsabilidades de estado con responsabilidades de negocio.

    Quién usa estas rules: session_service.py, antes de ejecutar operaciones
    que requieren validación de contexto, no solo de estado.

    Nota: todos los métodos son estáticos porque las rules no tienen estado propio.
    Son funciones de validación puras que reciben datos y retornan bool o lanzan excepciones.
    """

    @staticmethod
    def can_add_idea(session: Session) -> bool:
        """
        Determina si se puede agregar una nueva idea a la sesión.

        Regla: solo sesiones ACTIVE permiten nuevas ideas.
        Una sesión PAUSED, COMPLETED o ARCHIVED no debe aceptar ideas nuevas.

        Si esta regla retorna False y el servicio igual intenta crear una idea,
        session.register_new_idea() lanzará un ValueError como segunda línea de defensa.
        Se recomienda llamar esta rule ANTES de intentar la operación.
        """
        return session.status.is_editable()

    @staticmethod
    def can_be_completed(session: Session) -> bool:
        """
        Determina si la sesión puede marcarse como completada.

        Regla: debe tener al menos una idea registrada.
        No tiene sentido completar una sesión vacía; probablemente es un error del cliente.

        Si esto falla y el usuario sí creó ideas, revisar si session.total_ideas
        se está incrementando correctamente en session_service.py al crear ideas.
        """
        return session.total_ideas > 0 and session.status.can_transition_to(SessionStatus.COMPLETED)

    @staticmethod
    def can_be_archived(session: Session) -> bool:
        """
        Determina si la sesión puede archivarse.

        El archivado es el estado terminal: una sesión archivada no puede reabrirse.
        Solo se permite archivar desde PAUSED o COMPLETED, no desde ACTIVE directamente,
        para evitar perder trabajo en progreso por error.

        Si un usuario intenta archivar una sesión activa con trabajo en curso,
        el sistema debe pedirle que primero la pause o complete.
        """
        return session.status.can_transition_to(SessionStatus.ARCHIVED)

    @staticmethod
    def validate_title(title: str) -> None:
        """
        Valida que el título de una sesión cumpla las restricciones de negocio.

        Lanza ValueError con mensaje descriptivo si la validación falla.
        Centralizar aquí evita duplicar esta lógica en el endpoint y en el servicio.

        Si los usuarios reportan errores de validación confusos,
        los mensajes de error están aquí y son fáciles de ajustar.
        """
        if not title or not title.strip():
            raise ValueError("El título de la sesión no puede estar vacío.")
        if len(title.strip()) < 3:
            raise ValueError("El título de la sesión debe tener al menos 3 caracteres.")
        if len(title.strip()) > 150:
            raise ValueError("El título de la sesión no puede superar los 150 caracteres.")

    @staticmethod
    def assert_is_editable(session: Session) -> None:
        """
        Versión imperativa de can_add_idea: lanza excepción si la sesión no es editable.

        Usar este método en servicios donde el flujo debe detenerse si la sesión
        no está disponible para edición, en lugar de manejar un bool manualmente.

        Ejemplo de uso en session_service.py:
            SessionRules.assert_is_editable(session)  # lanza si no es editable
            idea = Idea.create(...)   # solo llega aquí si la sesión está activa
        """
        if not session.status.is_editable():
            raise ValueError(
                f"La sesión '{session.id}' está en estado '{session.status.value}' "
                f"y no acepta modificaciones. Solo las sesiones ACTIVE son editables."
            )