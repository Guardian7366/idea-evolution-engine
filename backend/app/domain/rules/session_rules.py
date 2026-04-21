"""
session_rules.py — Reglas de negocio para el ciclo de vida de una Session.

¿Por qué existe este archivo separado de la entidad Session?
- La entidad Session conoce su propio estado interno.
- SessionRules conoce las POLÍTICAS del negocio que pueden cambiar con el tiempo.
- Así podemos cambiar una regla sin tocar la entidad, y testear las reglas solas.

¿Quién usa estas reglas?
- session_service.py las llama antes de ejecutar operaciones sensibles.
- Si una regla falla, el servicio lanza un error que la API convierte en HTTP 400/409.

Regla de diseño: estos métodos NUNCA modifican nada. Solo validan.
"""

from app.domain.entities.session import Session


class SessionRules:

    @staticmethod
    def assert_is_editable(session: Session) -> None:
        """
        Verifica que la sesión está activa y puede recibir cambios.

        Úsala en session_service.assert_session_is_active() para cortar
        la ejecución inmediatamente si la sesión no es editable.

        Si lanza error: la sesión está en PAUSED, COMPLETED o ARCHIVED.
        """
        if not session.status.is_editable():
            raise ValueError(
                f"La sesión '{session.id}' está en estado '{session.status.value}' "
                "y no acepta modificaciones. Solo las sesiones ACTIVE pueden editarse."
            )

    @staticmethod
    def can_be_completed(session: Session) -> None:
        """
        Verifica que una sesión puede marcarse como completada.

        Condiciones:
        1. La sesión debe estar en ACTIVE.
        2. Debe tener al menos 1 idea registrada en session.idea_ids.

        ¿Por qué leemos session.idea_ids directamente en lugar de recibir
        un conteo como parámetro externo?
        Porque Session ya mantiene esa lista actualizada mediante add_idea().
        Leer desde la entidad elimina la posibilidad de pasar un conteo incorrecto.

        Si lanza "sin ideas": register_idea_added() en session_service no se llamó
        correctamente al crear ideas, o las ideas no se persisten bien.

        CAMBIO RESPECTO A SEMANA 1: antes se llamaba assert_can_be_completed y
        recibía total_ideas: int como parámetro. Ahora lee directamente de la
        entidad para mayor consistencia.
        """
        if session.status.value != "active":
            raise ValueError(
                f"Solo se puede completar una sesión ACTIVE. "
                f"Estado actual: '{session.status.value}'."
            )
        if not session.idea_ids:
            raise ValueError(
                "No se puede completar una sesión sin al menos una idea registrada. "
                "Verifica que idea_service esté llamando register_idea_added() correctamente."
            )