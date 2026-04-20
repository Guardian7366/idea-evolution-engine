from typing import List

from app.domain.entities.final_synthesis import FinalSynthesis
from app.domain.entities.idea_version import IdeaVersion
from app.domain.value_objects.version_status import VersionStatus


class SynthesisRules:
    """
    Reglas de negocio para la generación y validación de síntesis finales.

    ¿Qué problema resuelven?
    La síntesis es el paso más costoso en términos de tokens de IA y el más
    valioso para el usuario. Estas rules aseguran que solo se genera síntesis
    cuando el contexto lo justifica: la versión está lista, la idea tiene
    suficiente historial evolutivo, y no existe ya una síntesis reciente.

    Quién usa estas rules: synthesis_service.py, antes de invocar al modelo de IA
    para generar la síntesis final.
    """

    # Número mínimo de versiones iteradas recomendado antes de sintetizar.
    # Sintetizar con solo 1 versión es válido pero puede producir resultados poco profundos.
    # Si el producto decide que 1 iteración es suficiente, bajar este valor a 1.
    RECOMMENDED_MIN_VERSIONS = 2

    @staticmethod
    def can_synthesize(version: IdeaVersion) -> bool:
        """
        Determina si una versión específica está lista para generar síntesis final.

        Regla: la versión debe estar en estado SELECTED, lo que significa
        que el usuario ya eligió la variante ganadora de ese ciclo.

        Si retorna False para una versión que el usuario ya procesó,
        revisar que version_service.py esté avanzando el estado correctamente
        al llamar version.mark_variant_selected().
        """
        return version.status == VersionStatus.SELECTED

    @staticmethod
    def has_enough_iterations(versions: List[IdeaVersion]) -> bool:
        """
        Indica si la idea tiene suficientes versiones iteradas para una síntesis rica.

        Este método NO bloquea la síntesis (eso lo hace can_synthesize).
        Es informativo: el servicio puede usarlo para mostrar una advertencia
        al usuario si intenta sintetizar demasiado pronto.

        Ejemplo de uso en synthesis_service.py:
            if not SynthesisRules.has_enough_iterations(versions):
                # Mostrar advertencia, pero no bloquear
                logger.warning("Síntesis con pocas iteraciones para idea %s", idea_id)
        """
        completed_versions = [
            v for v in versions
            if v.status in {VersionStatus.SELECTED, VersionStatus.SYNTHESIZED}
        ]
        return len(completed_versions) >= SynthesisRules.RECOMMENDED_MIN_VERSIONS

    @staticmethod
    def is_valid_synthesis(synthesis: FinalSynthesis) -> bool:
        """
        Valida que una síntesis generada por la IA tenga el contenido mínimo esperado.

        Reglas:
          - Debe tener un título refinado no vacío.
          - Debe tener un contenido refinado no vacío.
          - Debe tener al menos una perspectiva clave O al menos un paso en el plan de acción.

        Una síntesis que pase estas reglas es apta para mostrarse al usuario.
        Si falla, la IA produjo una síntesis incompleta y el servicio debe reintentar.

        Si falla frecuentemente, revisar synthesis_prompts.py para asegurarse
        de que el prompt exige explícitamente perspectivas clave y plan de acción.
        """
        has_title = bool(synthesis.refined_title and synthesis.refined_title.strip())
        has_content = bool(synthesis.refined_content and synthesis.refined_content.strip())
        has_synthesis = len(synthesis.key_perspectives) > 0 or len(synthesis.action_plan) > 0
        return has_title and has_content and has_synthesis

    @staticmethod
    def assert_can_synthesize(version: IdeaVersion) -> None:
        """
        Versión imperativa de can_synthesize: lanza excepción si no se puede sintetizar.

        Usar en synthesis_service.py como primera validación antes de
        invocar al modelo de IA (evita gastar tokens si el estado es incorrecto).

        Ejemplo de uso:
            SynthesisRules.assert_can_synthesize(version)
            # Solo llega aquí si version.status == SELECTED
            synthesis = await ai_client.generate_synthesis(...)
        """
        if not SynthesisRules.can_synthesize(version):
            raise ValueError(
                f"La versión '{version.id}' está en estado '{version.status.value}' "
                "y no puede sintetizarse. La versión debe estar en estado SELECTED. "
                "Verificar que el usuario seleccionó una variante antes de solicitar síntesis."
            )

    @staticmethod
    def assert_is_valid(synthesis: FinalSynthesis) -> None:
        """
        Versión imperativa de is_valid_synthesis: lanza excepción si la síntesis es incompleta.

        Usar en synthesis_service.py después de recibir y mapear la respuesta de la IA,
        antes de persistir la síntesis.

        Ejemplo de uso:
            synthesis = FinalSynthesis.create(...)
            SynthesisRules.assert_is_valid(synthesis)  # lanza si está incompleta
            await synthesis_repository.save(synthesis)  # solo si es válida
        """
        if not SynthesisRules.is_valid_synthesis(synthesis):
            raise ValueError(
                f"La síntesis generada para la idea '{synthesis.idea_id}' está incompleta. "
                "Debe tener título, contenido y al menos una perspectiva o paso de acción. "
                "Revisar synthesis_prompts.py y synthesis_mapper.py en la capa de infraestructura."
            )
