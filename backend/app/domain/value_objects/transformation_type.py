from enum import Enum


class TransformationType(str, Enum):
    """
    Value Object que clasifica el tipo de transformación aplicada a una idea.
    Hereda de str para ser serializable directamente a JSON.

    IMPORTANTE: Estos valores están alineados con el DTO de la API (version_dto.py).
    El Literal del DTO es: "selection" | "evolve" | "refine" | "mutate".
    Si el DTO cambia sus valores, este enum debe actualizarse también.

    - SELECTION : La versión se creó porque el usuario seleccionó una variante
                  del conjunto inicial generado por la IA.
    - EVOLVE    : Evolución general de la idea hacia una dirección nueva.
                  Equivale conceptualmente a una expansión o mutación suave.
    - REFINE    : Mejora iterativa que mantiene la esencia original de la idea.
                  Ajusta detalles sin cambiar la dirección general.
    - MUTATE    : Cambio profundo en la naturaleza o enfoque de la idea.
                  Es la transformación más radical de las cuatro.
    """
    SELECTION = "selection"
    EVOLVE = "evolve"
    REFINE = "refine"
    MUTATE = "mutate"

    def is_structural(self) -> bool:
        """
        Retorna True si la transformación altera la estructura de la idea
        de forma profunda (no solo su contenido superficial).
        """
        return self in {TransformationType.MUTATE, TransformationType.EVOLVE}

    def is_incremental(self) -> bool:
        """
        Retorna True si la transformación es un ajuste iterativo sobre la idea base.
        """
        return self in {TransformationType.REFINE, TransformationType.SELECTION}

    def label(self) -> str:
        """Nombre legible en español para mostrar en UI o logs."""
        labels = {
            TransformationType.SELECTION: "Selección",
            TransformationType.EVOLVE:    "Evolución",
            TransformationType.REFINE:    "Refinamiento",
            TransformationType.MUTATE:    "Mutación",
        }
        return labels[self]