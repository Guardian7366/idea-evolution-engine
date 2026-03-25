from typing import List

from app.domain.entities.idea_version import IdeaVersion
from app.domain.value_objects.version_status import VersionStatus


class VersionRules:
    """
    Reglas de negocio para el ciclo de vida y flujo de evolución de IdeaVersions.

    ¿Qué problema resuelven?
    Una IdeaVersion avanza por varios estados (DRAFT → ANALYZING → ANALYZED → SELECTED → SYNTHESIZED).
    Estas rules validan si una versión está en el estado correcto para cada operación,
    y si el contexto global (ej: número de versiones existentes) lo permite.

    Quién usa estas rules: version_service.py, antes de ejecutar operaciones
    como iniciar análisis, seleccionar variante, o crear una nueva versión.
    """

    # Número máximo de versiones por idea antes de forzar síntesis.
    # Si una idea llega a este límite sin síntesis, el sistema puede
    # sugerir al usuario que cierre el ciclo en lugar de seguir iterando.
    MAX_VERSIONS_PER_IDEA = 10

    @staticmethod
    def can_start_analysis(version: IdeaVersion) -> bool:
        """
        Determina si una versión puede iniciar el proceso de análisis por IA.

        Regla: la versión debe estar en estado DRAFT.
        Si está en cualquier otro estado, el análisis ya fue iniciado o completado.

        Si retorna False para una versión recién creada, revisar que
        IdeaVersion.create() efectivamente inicializa el status en DRAFT.
        """
        return version.status.is_ready_for_analysis()

    @staticmethod
    def can_select_variant(version: IdeaVersion) -> bool:
        """
        Determina si la versión está lista para que el usuario seleccione una variante.

        Regla: la versión debe estar en estado ANALYZED.
        No se puede seleccionar una variante si el análisis no ha terminado.

        Si retorna False aunque la IA ya procesó la versión,
        revisar que analysis_service.py esté llamando version.advance_status(ANALYZED).
        """
        return version.status.is_ready_for_selection()

    @staticmethod
    def can_create_next_version(existing_versions: List[IdeaVersion]) -> bool:
        """
        Determina si se puede crear una nueva versión para una idea.

        Regla: no superar el máximo de versiones permitidas.
        Si se alcanza el límite, el sistema debe sugerir síntesis final
        en lugar de continuar iterando indefinidamente.

        Si este método siempre retorna False con pocas versiones,
        verificar que existing_versions no esté incluyendo versiones de otras ideas.
        """
        return len(existing_versions) < VersionRules.MAX_VERSIONS_PER_IDEA

    @staticmethod
    def get_latest_version(versions: List[IdeaVersion]) -> IdeaVersion | None:
        """
        Retorna la versión con el version_number más alto de la lista.

        Usar en idea_service.py o version_service.py para continuar el flujo
        desde la versión más reciente sin depender del orden de la lista.

        Si retorna None cuando se esperaba una versión, la lista está vacía,
        lo que indica que la idea no tiene versiones aún — revisar el flujo de creación.
        """
        if not versions:
            return None
        return max(versions, key=lambda v: v.version_number)

    @staticmethod
    def assert_can_start_analysis(version: IdeaVersion) -> None:
        """
        Versión imperativa de can_start_analysis: lanza excepción si no es posible.

        Usar en analysis_service.py al inicio del flujo de análisis.

        Ejemplo de uso:
            VersionRules.assert_can_start_analysis(version)
            # Solo llega aquí si version.status == DRAFT
            version.advance_status(VersionStatus.ANALYZING)
        """
        if not VersionRules.can_start_analysis(version):
            raise ValueError(
                f"La versión '{version.id}' está en estado '{version.status.value}' "
                f"y no puede iniciar análisis. Solo versiones en estado DRAFT pueden analizarse."
            )

    @staticmethod
    def assert_can_synthesize(version: IdeaVersion) -> None:
        """
        Valida que una versión esté en estado SELECTED antes de sintetizar.

        Usar en synthesis_service.py antes de generar la síntesis final.
        Si falla, significa que el usuario no seleccionó una variante,
        o que el flujo saltó un paso intermedio.
        """
        if version.status != VersionStatus.SELECTED:
            raise ValueError(
                f"La versión '{version.id}' debe estar en estado SELECTED para sintetizarse. "
                f"Estado actual: '{version.status.value}'. "
                "Verificar que el usuario seleccionó una variante antes de solicitar síntesis."
            )