from __future__ import annotations

from app.domain.entities.idea_variant import IdeaVariant
from app.shared.errors.domain_errors import VariantSelectionError


def ensure_variant_can_be_selected(variant: IdeaVariant) -> None:
    if variant.is_selected:
        raise VariantSelectionError("Variant has already been selected.")