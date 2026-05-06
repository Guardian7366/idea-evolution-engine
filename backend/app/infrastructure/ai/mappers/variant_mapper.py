from __future__ import annotations

from app.domain.entities.idea_variant import IdeaVariant


def map_variant_payloads_to_entities(
    payloads: list[dict],
    idea_id: str,
) -> list[IdeaVariant]:
    variants: list[IdeaVariant] = []

    for payload in payloads:
        variants.append(
            IdeaVariant(
                id=payload["id"],
                idea_id=idea_id,
                title=payload["title"],
                description=payload["description"],
                order_index=payload["order_index"],
                created_at=payload["created_at"],
                is_selected=False,
                selected_at=None,
            )
        )

    return variants