from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import uuid4


@dataclass
class VersionAnalysis:
    """
    Entidad que representa el análisis generado por la IA sobre una IdeaVersion específica.

    ¿Qué es un análisis en este sistema?
    Cuando una versión avanza del estado DRAFT → ANALYZING → ANALYZED,
    la IA evalúa la idea y produce:
      - fortalezas detectadas
      - debilidades detectadas
      - oportunidades de mejora
      - un score general de la idea

    Esta entidad guarda ese resultado de forma estructurada para que:
      1. El frontend pueda mostrarlo al usuario.
      2. Los servicios de síntesis puedan usarlo como input.
      3. Podamos comparar análisis entre versiones (ver VersionComparison).

    Relación con otras entidades:
      - Pertenece a exactamente una IdeaVersion (version_id).
      - Es generada por analysis_service.py después de recibir respuesta de la IA.
      - No modifica la versión directamente; solo la describe.
    """

    # Identificador único de este análisis.
    id: str

    # ID de la versión que fue analizada.
    # Si este campo no coincide con una IdeaVersion existente, hay un bug en analysis_service.py.
    version_id: str

    # ID de la idea padre. Redundante pero útil para queries directas sin joins.
    idea_id: str

    # Momento en que se completó el análisis.
    # Si created_at es muy distante del created_at de la versión,
    # puede indicar un cuello de botella en la IA o en la cola de procesamiento.
    created_at: datetime

    # Score numérico asignado por la IA a esta versión de la idea.
    # Rango esperado: 0.0 a 10.0.
    # Si recibes valores fuera de rango, el problema está en analysis_mapper.py (infra),
    # que es quien transforma la respuesta cruda de la IA a esta entidad.
    overall_score: float = 0.0

    # Lista de fortalezas identificadas por la IA.
    # Cada elemento es un string descriptivo. Ejemplo: "Clara propuesta de valor".
    # Si esta lista llega siempre vacía, revisar analysis_prompts.py en infra/ai/prompts/.
    strengths: List[str] = field(default_factory=list)

    # Lista de debilidades identificadas.
    # Mismo origen que strengths: viene procesada desde analysis_mapper.py.
    weaknesses: List[str] = field(default_factory=list)

    # Oportunidades de mejora sugeridas por la IA.
    # Estas alimentan directamente la generación de variantes en el siguiente ciclo evolutivo.
    # Si el motor de variantes no está generando sugerencias útiles, revisar este campo primero.
    opportunities: List[str] = field(default_factory=list)

    # Resumen narrativo del análisis en lenguaje natural.
    # Generado por la IA. Si es None, el análisis fue parcial o falló
    # en el paso de síntesis textual dentro del provider de IA.
    summary: Optional[str] = None

    @classmethod
    def create(
        cls,
        version_id: str,
        idea_id: str,
        overall_score: float,
        strengths: List[str],
        weaknesses: List[str],
        opportunities: List[str],
        summary: Optional[str] = None,
    ) -> "VersionAnalysis":
        """
        Factory method. Único punto válido para crear un análisis.

        ¿Por qué factory y no instanciar directo con VersionAnalysis(...)?
        Porque centralizamos validaciones aquí y asignamos el ID automáticamente.
        Si en el futuro se necesita auditoría o logging al crear análisis, se agrega aquí,
        sin tocar ningún otro archivo.

        Quién llama este método: analysis_service.py, después de recibir y parsear
        la respuesta de la IA a través de analysis_mapper.py.
        """
        if not (0.0 <= overall_score <= 10.0):
            raise ValueError(
                f"overall_score debe estar entre 0.0 y 10.0, se recibió: {overall_score}. "
                "Si este error aparece en producción, revisar analysis_mapper.py "
                "en app/infrastructure/ai/mappers/."
            )

        return cls(
            id=str(uuid4()),
            version_id=version_id,
            idea_id=idea_id,
            overall_score=overall_score,
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=opportunities,
            summary=summary,
            created_at=datetime.utcnow(),
        )

    def has_strong_score(self, threshold: float = 7.0) -> bool:
        """
        Indica si el análisis considera esta versión suficientemente buena.

        El threshold por defecto es 7.0, pero puede ajustarse por contexto de negocio.
        Usado en synthesis_service.py para decidir si una versión merece síntesis final.

        Si el sistema nunca produce síntesis aunque las ideas parecen buenas,
        puede ser que el score promedio de la IA sea bajo — ajustar threshold o los prompts.
        """
        return self.overall_score >= threshold

    def dominant_weakness_count(self) -> int:
        """
        Retorna cuántas debilidades fueron detectadas en este análisis.

        Si este número es consistentemente alto para todas las ideas,
        puede indicar que los prompts están siendo demasiado críticos.
        En ese caso, revisar analysis_prompts.py en infra/ai/prompts/.
        """
        return len(self.weaknesses)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, VersionAnalysis):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            f"VersionAnalysis(id={self.id!r}, version={self.version_id!r}, "
            f"score={self.overall_score}, strengths={len(self.strengths)}, "
            f"weaknesses={len(self.weaknesses)})"
        )