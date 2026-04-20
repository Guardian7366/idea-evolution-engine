from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from app.domain.entities import DateHelper


@dataclass
class VersionComparison(DateHelper):
    """
    Entidad que representa la comparación entre dos versiones de una misma idea.

    ¿Para qué sirve comparar versiones?
    El motor de evolución genera múltiples versiones de una idea a lo largo del tiempo.
    Esta entidad captura qué cambió entre una versión y otra, desde la perspectiva
    de la IA: qué mejoró, qué empeoró, y cuál es la versión recomendada.

    Esto permite al usuario entender el progreso de su idea de forma visual y narrativa,
    en lugar de tener que comparar manualmente dos bloques de texto.

    Relación con otras entidades:
      - Referencia dos IdeaVersion: version_a_id (anterior) y version_b_id (posterior).
      - Depende indirectamente de VersionAnalysis: los scores comparados
        vienen de los análisis de cada versión, procesados en analysis_service.py.
      - Es generada por analysis_service.py o un servicio dedicado de comparación.
      - No modifica ninguna versión; es solo una vista comparativa.

    Nota de diseño:
      Siempre se compara A → B donde A es la versión anterior y B la más reciente.
      Si version_a_id y version_b_id están invertidos, la comparación pierde sentido
      semántico (el "progreso" sería negativo aunque la idea haya mejorado).
    """

    # Identificador único de esta comparación.
    id: str

    # ID de la sesión a la que pertenecen ambas versiones.
    # Útil para filtrar comparaciones por sesión sin joins adicionales.
    session_id: str

    # ID de la idea que ambas versiones comparten.
    idea_id: str

    # Versión anterior (punto de partida de la comparación).
    # Siempre debe ser una versión con version_number menor que version_b.
    version_a_id: str

    # Versión posterior (resultado de la evolución).
    version_b_id: str

    # Momento en que se generó esta comparación.
    created_at: datetime

    # Score de la versión A, copiado desde su VersionAnalysis.
    # Si es 0.0 y no hay análisis previo, la comparación puede ser poco útil.
    score_a: float = 0.0

    # Score de la versión B.
    score_b: float = 0.0

    # Diferencia calculada: score_b - score_a.
    # Positivo = mejora. Negativo = regresión. Cero = sin cambio significativo.
    # Este campo se puede calcular en tiempo real con score_delta(), pero
    # se guarda para facilitar queries de ordenamiento sin recalcular.
    score_delta: float = 0.0

    # Aspectos que mejoraron al pasar de la versión A a la B.
    # Generado por la IA comparando ambos análisis.
    # Si siempre llega vacío, revisar synthesis_prompts.py o comparison_mapper.py.
    improvements: List[str] = field(default_factory=list)

    # Aspectos que empeoraron o se perdieron en la versión B respecto a la A.
    # Importante para detectar regresiones involuntarias en el flujo de evolución.
    regressions: List[str] = field(default_factory=list)

    # Resumen narrativo de la comparación generado por la IA.
    # Debe explicar en lenguaje natural qué evolucionó y por qué.
    # Si es None, la comparación fue generada sin pasar por el modelo de lenguaje
    # (puede ser una comparación simple basada solo en scores).
    narrative: Optional[str] = None

    # Versión recomendada por la IA: "a" o "b".
    # En la mayoría de casos debería ser "b", pero si la mutación fue demasiado agresiva
    # y empeoró la idea, la IA puede recomendar volver a "a".
    # Si este campo es None, la IA no pudo determinar una recomendación clara.
    recommended_version: Optional[str] = None

    @classmethod
    def create(
        cls,
        session_id: str,
        idea_id: str,
        version_a_id: str,
        version_b_id: str,
        score_a: float,
        score_b: float,
        improvements: List[str],
        regressions: List[str],
        narrative: Optional[str] = None,
        recommended_version: Optional[str] = None,
    ) -> "VersionComparison":
        """
        Factory method. Único punto válido para crear una comparación.

        Calcula automáticamente score_delta para no depender de que el llamador
        lo calcule correctamente (evita inconsistencias entre score_delta
        y los valores reales de score_a / score_b).

        Quién llama este método: analysis_service.py o un futuro comparison_service.py,
        después de recuperar los análisis de ambas versiones.
        """
        if version_a_id == version_b_id:
            raise ValueError(
                "version_a_id y version_b_id no pueden ser iguales. "
                "No tiene sentido comparar una versión consigo misma."
            )

        if recommended_version not in (None, "a", "b"):
            raise ValueError(
                f"recommended_version debe ser 'a', 'b' o None, se recibió: {recommended_version!r}."
            )

        return cls(
            id=str(uuid4()),
            session_id=session_id,
            idea_id=idea_id,
            version_a_id=version_a_id,
            version_b_id=version_b_id,
            score_a=score_a,
            score_b=score_b,
            # Delta calculado aquí para garantizar consistencia interna.
            score_delta=round(score_b - score_a, 2),
            improvements=improvements,
            regressions=regressions,
            narrative=narrative,
            recommended_version=recommended_version,
            created_at=datetime.utcnow(),
        )

    def is_improvement(self) -> bool:
        """
        Retorna True si la versión B es mejor que la A según los scores.

        Umbral mínimo de 0.1 para evitar falsos positivos por diferencias
        de decimales sin significado real (ej: 7.0 vs 7.05).
        Si el sistema reporta mejoras cuando visualmente no las hay,
        revisar cómo la IA asigna scores en analysis_prompts.py.
        """
        return self.score_delta > 0.1

    def is_regression(self) -> bool:
        """
        Retorna True si la versión B es peor que la A.
        Útil para alertar al usuario o al sistema que la evolución retrocedió.
        """
        return self.score_delta < -0.1

    def has_regressions(self) -> bool:
        """
        Retorna True si la IA detectó aspectos que empeoraron,
        independientemente del score general.
        Una idea puede mejorar en score pero perder alguna cualidad específica.
        """
        return len(self.regressions) > 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VersionComparison):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            f"VersionComparison(id={self.id!r}, "
            f"a={self.version_a_id!r} → b={self.version_b_id!r}, "
            f"delta={self.score_delta:+.2f}, recommended={self.recommended_version!r})"
        )
