from enum import Enum


class TransformationType(str, Enum):
    """
    Value Object que representa el tipo de transformación aplicada a una idea.
    Cada tipo guía al motor de IA sobre qué clase de evolución realizar.
    """
    # Genera variantes divergentes de la idea original
    MUTATION = "mutation"

    # Refina la idea enfocándola o mejorando su claridad
    REFINEMENT = "refinement"

    # Combina elementos de múltiples variantes en una síntesis
    SYNTHESIS = "synthesis"

    # Explora el opuesto o contraste de la idea
    INVERSION = "inversion"

    # Amplía el alcance o escala de la idea
    EXPANSION = "expansion"

    def requires_variants(self) -> bool:
        """
        Indica si el tipo de transformación necesita variantes previas
        como input (no puede aplicarse sobre una idea vacía).
        """
        return self in {TransformationType.SYNTHESIS}

    def is_divergent(self) -> bool:
        """Indica si la transformación produce múltiples variantes."""
        return self in {TransformationType.MUTATION, TransformationType.EXPANSION}