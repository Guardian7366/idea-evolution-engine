"""
version_rules.py — Reglas de negocio para el ciclo de vida de IdeaVersions.

¿Qué controla este archivo?
- Si se puede crear una nueva versión para una idea (límite de 10).
- Si una versión puede avanzar al siguiente estado del pipeline.
- Utilitarios para obtener la versión más reciente de una lista.

¿Quién usa estas reglas?
- version_service.py antes de crear o avanzar versiones.

Estados válidos del pipeline (definidos en VersionStatus):
    DRAFT → ANALYZED → SELECTED → SUPERSEDED

CAMBIOS RESPECTO A SEMANA 1: 
- Se eliminaron assert_can_create_new_version(), assert_can_start_analysis(),
  assert_can_select_variant() y assert_can_synthesize() porque duplicaban
  lógica que ya vive en IdeaVersion._transition_to() via mark_analyzed(),
  mark_selected() y supersede(). La entidad ya lanza ValueError con mensaje
  claro si la transición no es válida.
- Se eliminó is_ready_for_analysis() e is_ready_for_selection() porque
  VersionStatus real no tiene esos métodos (solo tiene can_transition_to e is_active).
- can_create_next_version() ahora recibe List[IdeaVersion] en lugar de int,
  alineado con cómo version_service lo llama realmente.
"""

from typing import List, Optional

from app.domain.entities.idea_version import IdeaVersion


class VersionRules:
    """
    Reglas de negocio para versiones de ideas.

    Todos los métodos son estáticos — no necesitan instancia.
    """

    # Número máximo de versiones por idea antes de forzar síntesis.
    # Si una idea llega a este límite, el sistema debe sugerir al usuario
    # cerrar el ciclo evolutivo en lugar de seguir iterando.
    # Ajustar este valor aquí afecta a todo el sistema automáticamente.
    MAX_VERSIONS_PER_IDEA = 10

    @staticmethod
    def can_create_next_version(existing_versions: List[IdeaVersion]) -> bool:
        """
        ¿Se puede crear una versión más para esta idea?

        Recibe la lista completa de versiones existentes (no un conteo)
        para que el llamador no tenga que hacer la cuenta manualmente.

        Si retorna False: la idea ya tiene MAX_VERSIONS_PER_IDEA versiones.
        version_service debe informar al usuario que genere una síntesis final.

        Si siempre retorna False con pocas versiones: verificar que
        existing_versions no esté incluyendo versiones de otras ideas.
        El filtro por idea_id debe hacerse antes de llamar este método.
        """
        return len(existing_versions) < VersionRules.MAX_VERSIONS_PER_IDEA

    @staticmethod
    def get_latest_version(versions: List[IdeaVersion]) -> Optional[IdeaVersion]:
        """
        Retorna la versión con el version_number más alto de la lista.

        Retorna None si la lista está vacía, lo que indica que la idea
        no tiene versiones todavía — revisar el flujo de creación en idea_service.

        Se usa en version_service.get_latest_version() para continuar
        el flujo desde la versión más reciente sin depender del orden de la lista.
        """
        if not versions:
            return None
        return max(versions, key=lambda v: v.version_number)

    @staticmethod
    def get_active_version(versions: List[IdeaVersion]) -> Optional[IdeaVersion]:
        """
        Retorna la versión activa actual de una idea.

        Una versión está activa si su status no es SUPERSEDED
        (definido en VersionStatus.is_active()).

        En un flujo correcto debería haber como máximo UNA versión activa
        por idea en cualquier momento. Si hay más de una, hay un bug en
        version_service que no está marcando las versiones anteriores
        como SUPERSEDED al crear nuevas.

        Retorna None si todas las versiones están SUPERSEDED
        (situación inusual que indicaría que el flujo se cerró sin síntesis).
        """
        active = [v for v in versions if v.status.is_active()]
        if not active:
            return None
        # Si por algún bug hay más de una activa, retornamos la más reciente.
        return max(active, key=lambda v: v.version_number)