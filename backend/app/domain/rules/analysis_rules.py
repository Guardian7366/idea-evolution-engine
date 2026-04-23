"""
analysis_rules.py — Reglas de negocio para VersionAnalysis.

Actúan como filtro entre la IA y el resto del dominio:
aseguran que solo análisis con contenido real avanzan en el flujo.

¿Quién usa estas rules?
analysis_service.py, justo después de recibir y mapear la respuesta de la IA,
antes de persistir el análisis.

Este archivo está alineado con VersionAnalysis real:
- overall_score: float (rango 0.0 a 10.0)
- strengths: List[str]
- weaknesses: List[str]
- version_id: str
"""

from app.domain.entities.version_analysis import VersionAnalysis


class AnalysisRules:

    # Score mínimo para que tenga sentido generar variantes en el siguiente ciclo.
    # Si una idea tiene score muy bajo, puede ser mejor pedirle al usuario
    # que reescriba la idea en lugar de generar variantes poco útiles.
    MIN_SCORE_FOR_VARIANTS = 3.0

    # Score mínimo para recomendar cerrar el ciclo con síntesis final.
    # Evita que el usuario itere indefinidamente una idea que ya es buena.
    MIN_SCORE_FOR_SYNTHESIS = 7.0

    @staticmethod
    def is_valid_analysis(analysis: VersionAnalysis) -> bool:
        """
        Valida que un análisis tenga el mínimo de contenido útil para avanzar en el flujo.

        Condiciones:
        - Debe tener al menos una fortaleza O al menos una debilidad.
        - El score debe estar entre 0.0 y 10.0.

        Si esto falla frecuentemente en producción, revisar:
        1. analysis_prompts.py: ¿el prompt pide explícitamente fortalezas y debilidades?
        2. analysis_mapper.py: ¿está parseando bien la respuesta de la IA?
        """
        has_content = len(analysis.strengths) > 0 or len(analysis.weaknesses) > 0
        valid_score = 0.0 <= analysis.overall_score <= 10.0
        return has_content and valid_score

    @staticmethod
    def should_generate_variants(analysis: VersionAnalysis) -> bool:
        """
        ¿El análisis justifica generar variantes para el siguiente ciclo?

        Si el sistema nunca genera variantes, bajar MIN_SCORE_FOR_VARIANTS
        o revisar si los scores de la IA son consistentemente bajos.
        """
        return analysis.overall_score >= AnalysisRules.MIN_SCORE_FOR_VARIANTS

    @staticmethod
    def should_recommend_synthesis(analysis: VersionAnalysis) -> bool:
        """
        ¿El análisis es tan positivo que conviene recomendar síntesis final ya?

        El servicio puede usar esto para mostrar una sugerencia proactiva al usuario.
        Si el sistema siempre recomienda síntesis prematuramente, subir MIN_SCORE_FOR_SYNTHESIS.
        """
        return analysis.overall_score >= AnalysisRules.MIN_SCORE_FOR_SYNTHESIS

    @staticmethod
    def assert_is_valid(analysis: VersionAnalysis) -> None:
        """
        Versión "assert" de is_valid_analysis: lanza ValueError si el análisis no es válido.

        Usar en analysis_service.py después de crear el análisis con VersionAnalysis.create().
        Detiene el flujo si la IA retornó datos insuficientes.

        Si lanza error: la IA devolvió un análisis vacío.
        Primer lugar donde buscar el bug: analysis_prompts.py y analysis_mapper.py.
        """
        if not AnalysisRules.is_valid_analysis(analysis):
            raise ValueError(
                f"El análisis de la versión '{analysis.version_id}' está incompleto "
                "(sin fortalezas ni debilidades). "
                "Revisar analysis_prompts.py y analysis_mapper.py en infrastructure/ai/."
            )