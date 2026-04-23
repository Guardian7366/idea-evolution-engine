"""
synthesis_rules.py — Reglas de negocio para FinalSynthesis.

Aseguran que la síntesis solo se genera cuando el contexto lo justifica
y que el resultado de la IA es válido antes de persistirlo.

¿Quién usa estas rules?
synthesis_service.py, antes y después de invocar al modelo de IA.

CORRECCIONES RESPECTO A LA VERSIÓN ANTERIOR: (BORRAR EN LOS SIGUIENTES CAMBIOS)

1. has_enough_iterations() usaba VersionStatus.SYNTHESIZED que NO existe
   en el VersionStatus real del proyecto (solo hay DRAFT, ANALYZED, SELECTED,
   SUPERSEDED). Se reemplazó por SUPERSEDED, que es el estado al que llega
   una versión cuando fue reemplazada por una nueva — lo que equivale a
   "esta versión ya fue procesada y el flujo siguió adelante".

2. can_synthesize() mencionaba version.mark_variant_selected() en su docstring
   pero ese método no existe en IdeaVersion. El método real es mark_selected().
   Se corrigió la referencia en el comentario.
"""

from typing import List

from app.domain.entities.final_synthesis import FinalSynthesis
from app.domain.entities.idea_version import IdeaVersion
from app.domain.value_objects.version_status import VersionStatus


class SynthesisRules:

    # Número mínimo de versiones procesadas recomendado antes de sintetizar.
    # No bloquea la síntesis — es informativo para mostrar advertencias al usuario.
    # Si el producto decide que 1 iteración es suficiente, bajar este valor a 1.
    RECOMMENDED_MIN_VERSIONS = 2

    @staticmethod
    def can_synthesize(version: IdeaVersion) -> bool:
        """
        ¿Esta versión está lista para generar síntesis final?

        La versión debe estar en SELECTED: el usuario ya eligió
        la variante ganadora de ese ciclo evolutivo.

        Si retorna False para una versión que el usuario ya procesó,
        revisar que version_service.py esté llamando mark_selected()
        correctamente después de que el usuario elige una variante.
        """
        return version.status == VersionStatus.SELECTED

    @staticmethod
    def has_enough_iterations(versions: List[IdeaVersion]) -> bool:
        """
        ¿La idea tiene suficientes versiones procesadas para una síntesis rica?

        Este método NO bloquea la síntesis — es informativo.
        El servicio puede usarlo para registrar un warning si el usuario
        intenta sintetizar con muy pocas iteraciones.

        CORRECCIÓN: la versión anterior filtraba por SYNTHESIZED que no existe
        en VersionStatus. Ahora filtramos por SUPERSEDED (versiones que ya fueron
        reemplazadas por otras nuevas, lo que indica iteración real) más SELECTED
        (la versión activa actual que está lista para sintetizar).
        """
        processed = [
            v for v in versions
            if v.status in {VersionStatus.SELECTED, VersionStatus.SUPERSEDED}
        ]
        return len(processed) >= SynthesisRules.RECOMMENDED_MIN_VERSIONS

    @staticmethod
    def is_valid_synthesis(synthesis: FinalSynthesis) -> bool:
        """
        ¿La síntesis generada por la IA tiene el contenido mínimo esperado?

        Condiciones:
        - Título refinado no vacío.
        - Contenido refinado no vacío.
        - Al menos una perspectiva clave O al menos un paso en el plan de acción.

        Si falla frecuentemente, revisar synthesis_prompts.py para asegurarse
        de que el prompt pide explícitamente perspectivas y plan de acción.
        """
        has_title = bool(synthesis.refined_title and synthesis.refined_title.strip())
        has_content = bool(synthesis.refined_content and synthesis.refined_content.strip())
        has_synthesis = len(synthesis.key_perspectives) > 0 or len(synthesis.action_plan) > 0
        return has_title and has_content and has_synthesis

    @staticmethod
    def assert_can_synthesize(version: IdeaVersion) -> None:
        """
        Versión "assert" de can_synthesize.
        Lanza ValueError si la versión no está lista para sintetizar.

        Usar en synthesis_service.py como primera validación antes de
        llamar a la IA — evita gastar tokens si el estado es incorrecto.
        """
        if not SynthesisRules.can_synthesize(version):
            raise ValueError(
                f"La versión '{version.id}' está en estado '{version.status.value}' "
                "y no puede sintetizarse. Debe estar en SELECTED. "
                "Verificar que el usuario seleccionó una variante antes de solicitar síntesis."
            )

    @staticmethod
    def assert_is_valid(synthesis: FinalSynthesis) -> None:
        """
        Versión "assert" de is_valid_synthesis.
        Lanza ValueError si la síntesis generada por la IA está incompleta.

        Usar en synthesis_service.py después de recibir y mapear la respuesta
        de la IA, antes de persistir la síntesis.
        """
        if not SynthesisRules.is_valid_synthesis(synthesis):
            raise ValueError(
                f"La síntesis de la idea '{synthesis.idea_id}' está incompleta. "
                "Debe tener título, contenido y al menos una perspectiva o paso de acción. "
                "Revisar synthesis_prompts.py y synthesis_mapper.py en infrastructure/ai/."
            )