from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from app.domain.entities import DateHelper


@dataclass
class FinalSynthesis(DateHelper):
    """
    Entidad que representa la síntesis final generada al cerrar el ciclo evolutivo de una idea.

    ¿Qué es la síntesis final?
    Es el documento conclusivo que la IA produce después de que el usuario
    ha iterado suficientes veces sobre una idea. Consolida:
      - La versión más fuerte de la idea.
      - Las perspectivas más valiosas descubiertas durante la evolución.
      - Un plan de acción concreto para implementarla.
      - Una evaluación de viabilidad.

    Es el entregable final que el usuario se lleva de la sesión.

    Relación con otras entidades:
      - Pertenece a una Session (session_id) y a una Idea (idea_id).
      - Referencia la IdeaVersion que se considera la mejor (best_version_id).
      - Es generada por synthesis_service.py después de que el usuario
        decide cerrar el ciclo evolutivo o cuando se alcanza un score alto.
      - Una sesión puede tener múltiples síntesis si el usuario evolucionó
        varias ideas distintas dentro de la misma sesión.

    Nota de diseño:
      Esta entidad es inmutable en la práctica: una vez generada, no debería
      modificarse. Si el usuario quiere refinar más, debe crear una nueva versión
      y eventualmente una nueva síntesis. No hay método update() aquí por diseño.
    """

    # Identificador único de esta síntesis.
    id: str

    # ID de la sesión donde ocurrió la evolución.
    session_id: str

    # ID de la idea que fue sintetizada.
    idea_id: str

    # ID de la versión considerada la mejor al momento de sintetizar.
    # Si este ID no existe en la base de datos, hay un bug en synthesis_service.py.
    best_version_id: str

    # Momento en que se generó la síntesis.
    created_at: datetime

    # Título refinado de la idea en su forma final.
    # Puede diferir del título original: la IA puede proponer un nombre más preciso.
    # Si siempre es igual al título original, revisar synthesis_prompts.py.
    refined_title: str

    # Contenido consolidado y pulido de la idea en su mejor versión.
    # Este es el campo más importante de la síntesis para el usuario.
    refined_content: str

    # Número de versiones que se iteraron antes de llegar a esta síntesis.
    # Útil para mostrar al usuario cuánto evolucionó su idea.
    # Si este valor es siempre 1, puede indicar que el flujo de selección
    # no está funcionando correctamente y está cerrando el ciclo demasiado pronto.
    total_versions_iterated: int = 0

    # Score final de la mejor versión, copiado desde su VersionAnalysis.
    # Si es 0.0 en producción, revisar que synthesis_service.py
    # esté recuperando el análisis antes de crear la síntesis.
    final_score: float = 0.0

    # Perspectivas clave descubiertas durante todo el proceso evolutivo.
    # Consolida los insights más valiosos de todos los análisis de versiones.
    # Generado por la IA comparando el historial de análisis.
    key_perspectives: List[str] = field(default_factory=list)

    # Pasos de acción concretos que la IA recomienda para implementar la idea.
    # Si esta lista llega vacía, revisar synthesis_prompts.py para asegurarse
    # de que el prompt pide explícitamente un plan de acción estructurado.
    action_plan: List[str] = field(default_factory=list)

    # Evaluación de viabilidad en lenguaje natural.
    # Ejemplo: "Alta viabilidad técnica, complejidad de mercado media."
    # Si es None, la IA no generó este apartado — revisar el prompt de síntesis.
    viability_assessment: Optional[str] = None

    # Notas adicionales o advertencias que la IA quiso destacar.
    # Ejemplo: "Esta idea requiere validación regulatoria antes de implementarse."
    additional_notes: Optional[str] = None

    @classmethod
    def create(
        cls,
        session_id: str,
        idea_id: str,
        best_version_id: str,
        refined_title: str,
        refined_content: str,
        total_versions_iterated: int,
        final_score: float,
        key_perspectives: List[str],
        action_plan: List[str],
        viability_assessment: Optional[str] = None,
        additional_notes: Optional[str] = None,
    ) -> "FinalSynthesis":
        """
        Factory method. Único punto válido para crear una síntesis final.

        Valida que los campos críticos tengan contenido real antes de persistir,
        porque una síntesis vacía no tiene valor para el usuario y puede
        indicar un fallo silencioso en el pipeline de IA.

        Quién llama este método: synthesis_service.py, después de recopilar
        el historial de versiones y análisis y enviarlo al modelo de lenguaje
        a través de synthesis_prompts.py.
        """
        if not refined_title or not refined_title.strip():
            raise ValueError(
                "refined_title no puede estar vacío en una síntesis final. "
                "Revisar synthesis_prompts.py y synthesis_mapper.py."
            )

        if not refined_content or not refined_content.strip():
            raise ValueError(
                "refined_content no puede estar vacío en una síntesis final. "
                "Revisar synthesis_prompts.py y synthesis_mapper.py."
            )

        if total_versions_iterated < 1:
            raise ValueError(
                "total_versions_iterated debe ser al menos 1. "
                "No puede existir una síntesis sin al menos una versión iterada."
            )

        if not (0.0 <= final_score <= 10.0):
            raise ValueError(
                f"final_score debe estar entre 0.0 y 10.0, se recibió: {final_score}. "
                "Revisar analysis_mapper.py o cómo synthesis_service.py recupera el score."
            )

        return cls(
            id=str(uuid4()),
            session_id=session_id,
            idea_id=idea_id,
            best_version_id=best_version_id,
            refined_title=refined_title,
            refined_content=refined_content,
            total_versions_iterated=total_versions_iterated,
            final_score=final_score,
            key_perspectives=key_perspectives,
            action_plan=action_plan,
            viability_assessment=viability_assessment,
            additional_notes=additional_notes,
            created_at=datetime.utcnow(),
        )

    def is_high_quality(self, threshold: float = 7.5) -> bool:
        """
        Indica si esta síntesis alcanzó un nivel de calidad alto según el score final.

        Threshold más estricto que en VersionAnalysis (7.5 vs 7.0) porque
        la síntesis final representa el mejor resultado posible del ciclo completo.
        Si el sistema nunca marca síntesis como high_quality, bajar el threshold
        o revisar cómo la IA asigna scores finales.
        """
        return self.final_score >= threshold

    def has_action_plan(self) -> bool:
        """
        Verifica si la síntesis incluye un plan de acción.
        El frontend puede usar esto para mostrar u ocultar la sección de pasos.
        Si siempre es False, es un problema en synthesis_prompts.py.
        """
        return len(self.action_plan) > 0

    def evolution_depth(self) -> str:
        """
        Retorna una descripción legible de qué tan profundo fue el proceso evolutivo,
        basada en la cantidad de versiones iteradas.

        Útil para mostrar al usuario un resumen del proceso.
        """
        if self.total_versions_iterated == 1:
            return "Exploración inicial"
        elif self.total_versions_iterated <= 3:
            return "Evolución básica"
        elif self.total_versions_iterated <= 6:
            return "Evolución intermedia"
        else:
            return "Evolución profunda"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FinalSynthesis):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            f"FinalSynthesis(id={self.id!r}, idea={self.idea_id!r}, "
            f"score={self.final_score}, versions={self.total_versions_iterated}, "
            f"title={self.refined_title!r})"
        )
