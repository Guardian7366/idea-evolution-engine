from __future__ import annotations

from datetime import datetime
from sqlalchemy.orm import Session as DBSession

from app.domain.entities.idea import Idea
from app.domain.entities.idea_variant import IdeaVariant
from app.domain.repositories.idea_repository import IdeaRepository
from app.domain.value_objects.idea_content import IdeaContent
from app.infrastructure.persistence.models.idea_model import IdeaModel
from app.infrastructure.persistence.models.version_model import IdeaVariantModel
from datetime import datetime, timezone

class SqliteIdeaRepository(IdeaRepository):
    def __init__(self, db: DBSession) -> None:
        self.db = db

    def save_idea(self, idea: Idea) -> Idea:
        model = IdeaModel(
            id=idea.id,
            session_id=idea.session_id,
            title=idea.title,
            content=idea.content.value,
            created_at=idea.created_at.isoformat(),
            updated_at=idea.updated_at.isoformat(),
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return Idea(
            id=model.id,
            session_id=model.session_id,
            title=model.title,
            content=IdeaContent(model.content),
            created_at=idea.created_at,
            updated_at=idea.updated_at,
        )

    def get_idea_by_id(self, idea_id: str) -> Idea | None:
        model = self.db.query(IdeaModel).filter(IdeaModel.id == idea_id).first()
        if model is None:
            return None

        return Idea(
            id=model.id,
            session_id=model.session_id,
            title=model.title,
            content=IdeaContent(model.content),
            created_at=datetime.fromisoformat(model.created_at),
            updated_at=datetime.fromisoformat(model.updated_at),
        )

    def save_variants(self, variants: list[IdeaVariant]) -> list[IdeaVariant]:
        for variant in variants:
            model = IdeaVariantModel(
                id=variant.id,
                idea_id=variant.idea_id,
                title=variant.title,
                description=variant.description,
                order_index=variant.order_index,
                is_selected=variant.is_selected,
                selected_at=variant.selected_at.isoformat() if variant.selected_at else None,
                created_at=variant.created_at.isoformat(),
            )
            self.db.add(model)

        self.db.commit()
        return variants

    def list_variants_by_idea_id(self, idea_id: str) -> list[IdeaVariant]:
        models = (
            self.db.query(IdeaVariantModel)
            .filter(IdeaVariantModel.idea_id == idea_id)
            .order_by(IdeaVariantModel.order_index.asc())
            .all()
        )

        return [self._to_variant_entity(model) for model in models]

    def get_variant_by_id(self, variant_id: str) -> IdeaVariant | None:
        model = (
            self.db.query(IdeaVariantModel)
            .filter(IdeaVariantModel.id == variant_id)
            .first()
        )
        if model is None:
            return None
        return self._to_variant_entity(model)

    def mark_variant_selected(self, variant_id: str) -> IdeaVariant | None:
        model = (
            self.db.query(IdeaVariantModel)
            .filter(IdeaVariantModel.id == variant_id)
            .first()
        )
        if model is None:
            return None

        model.is_selected = True
        model.selected_at = datetime.now(timezone.utc).isoformat()
        self.db.commit()
        self.db.refresh(model)

        return self._to_variant_entity(model)

    def _to_variant_entity(self, model: IdeaVariantModel) -> IdeaVariant:
        return IdeaVariant(
            id=model.id,
            idea_id=model.idea_id,
            title=model.title,
            description=model.description,
            order_index=model.order_index,
            is_selected=model.is_selected,
            selected_at=datetime.fromisoformat(model.selected_at) if model.selected_at else None,
            created_at=datetime.fromisoformat(model.created_at),
        )