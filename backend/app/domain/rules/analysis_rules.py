from typing import List

from app.domain.entities.version_analysis import VersionAnalysis


class AnalysisRules:
    """
    Reglas de negocio para la validación y uso de VersionAnalysis.

    ¿Qué problema resuelven?
    El análisis es generado por la IA, lo que significa que su contenido
    puede ser incompleto, inconsistente o estar fuera de los rangos esperados.
    Estas rules actúan como una capa de validación entre la infraestructura de IA
    y el resto del dominio, asegurando que solo análisis válidos avanzan en el flujo.

    Quién usa estas rules: analysis_service.py, justo después de recibir
    y mapear la respuesta de la IA, antes de persistir el análisis.
    """

    # Score mínimo para considerar que un análisis tiene suficiente calidad
    # para generar variantes útiles en el siguiente ciclo evolutivo.
    # Si se baja este umbral, el sistema generará variantes incluso para ideas muy débiles.
    MIN_SCORE_FOR_VARIANTS = 3.0

    # Score mínimo para recomendar síntesis final directamente.
    # Una idea que supere este umbral puede cerrarse sin más iteraciones.
    MIN_SCORE_FOR_SYNTHESIS = 7.0

    @staticmethod
    def is_valid_analysis(analysis: VersionAnalysis) -> bool:
        """
        Valida que un análisis tenga el mínimo de contenido útil.

        Reglas:
          - Debe tener al menos una fortaleza O al menos una debilidad.
          - El score debe estar en el rango válido (0.0 a 10.0).

        Un análisis completamente vacío (sin fortalezas ni debilidades) indica
        que la IA retornó una respuesta incompleta. En ese caso, el servicio
        debe reintentar o marcar la versión como fallida.

        Si este método falla frecuentemente en producción, revisar:
          1. analysis_prompts.py: ¿el prompt pide explícitamente fortalezas y debilidades?
          2. analysis_mapper.py: ¿está parseando correctamente la respuesta de la IA?
        """
        has_content = len(analysis.strengths) > 0 or len(analysis.weaknesses) > 0
        valid_score = 0.0 <= analysis.overall_score <= 10.0
        return has_content and valid_score

    @staticmethod
    def should_generate_variants(analysis: VersionAnalysis) -> bool:
        """
        Determina si el análisis justifica generar variantes para el siguiente ciclo.

        Regla: el score debe superar el mínimo configurado.
        Si una idea tiene un score muy bajo, generar variantes puede ser un desperdicio
        de tokens de IA. En ese caso, puede ser mejor pedir al usuario que reescriba la idea.

        Si el sistema nunca genera variantes, bajar MIN_SCORE_FOR_VARIANTS
        o revisar si los scores de la IA están siendo demasiado bajos consistentemente.
        """
        return analysis.overall_score >= AnalysisRules.MIN_SCORE_FOR_VARIANTS

    @staticmethod
    def should_recommend_synthesis(analysis: VersionAnalysis) -> bool:
        """
        Determina si el análisis es tan positivo que se puede recomendar
        cerrar el ciclo con síntesis final sin más iteraciones.

        Esto evita que el usuario itere indefinidamente una idea que ya es buena.
        El servicio puede usar esto para mostrar una sugerencia proactiva en el frontend.

        Si el sistema siempre recomienda síntesis prematuramente,
        subir el valor de MIN_SCORE_FOR_SYNTHESIS.
        """
        return analysis.overall_score >= AnalysisRules.MIN_SCORE_FOR_SYNTHESIS

    @staticmethod
    def assert_is_valid(analysis: VersionAnalysis) -> None:
        """
        Versión imperativa de is_valid_analysis: lanza excepción si el análisis no es válido.

        Usar en analysis_service.py después de crear el análisis con VersionAnalysis.create().
        Detiene el flujo si la IA retornó datos insuficientes.

        Ejemplo de uso:
            analysis = VersionAnalysis.create(...)
            AnalysisRules.assert_is_valid(analysis)  # lanza si está vacío
            await analysis_repository.save(analysis)  # solo llega aquí si es válido
        """
        if not AnalysisRules.is_valid_analysis(analysis):
            raise ValueError(
                f"El análisis generado para la versión '{analysis.version_id}' no tiene "
                "contenido suficiente (sin fortalezas ni debilidades). "
                "Revisar analysis_prompts.py y analysis_mapper.py en la capa de infraestructura."
            )