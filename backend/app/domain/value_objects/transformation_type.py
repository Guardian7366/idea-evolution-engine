from __future__ import annotations

from enum import Enum


class TransformationType(str, Enum):
    VARIANT_SELECTION = "variant_selection"
    EVOLUTION = "evolution"
    REFINEMENT = "refinement"
    MUTATION = "mutation"