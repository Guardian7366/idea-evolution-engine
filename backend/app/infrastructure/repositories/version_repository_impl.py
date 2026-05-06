from __future__ import annotations

from datetime import datetime
from sqlalchemy.orm import Session as DBSession

from app.domain.entities.idea_version import IdeaVersion
from app.domain.repositories.version_repository import VersionRepository
from app.domain.value_objects.transformation_type import TransformationType
from app.domain.value_objects.version_status import VersionStatus
from app.infrastructure.persistence.models.version_model import IdeaVersionModel
from datetime import datetime, timezone

class SqliteVersionRepository(VersionRepository):
    def __init__(self, db: DBSession) -> None:
        self.db = db

    def save(self, version: IdeaVersion) -> IdeaVersion:
        model = IdeaVersionModel(
            id=version.id,
            idea_id=version.idea_id,
            source_variant_id=version.source_variant_id,
            parent_version_id=version.parent_version_id,
            content=version.content,
            version_number=version.version_number,
            transformation_type=version.transformation_type.value,
            user_instruction=version.user_instruction,
            is_active=version.is_active,
            status=version.status.value,
            created_at=version.created_at.isoformat(),
            updated_at=version.updated_at.isoformat(),
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return self._to_entity(model)

    def list_by_idea_id(self, idea_id: str) -> list[IdeaVersion]:
        models = (
            self.db.query(IdeaVersionModel)
            .filter(IdeaVersionModel.idea_id == idea_id)
            .order_by(IdeaVersionModel.version_number.asc())
            .all()
        )
        return [self._to_entity(model) for model in models]

    def get_by_id(self, version_id: str) -> IdeaVersion | None:
        model = (
            self.db.query(IdeaVersionModel)
            .filter(IdeaVersionModel.id == version_id)
            .first()
        )
        if model is None:
            return None
        return self._to_entity(model)

    def get_active_by_idea_id(self, idea_id: str) -> IdeaVersion | None:
        model = (
            self.db.query(IdeaVersionModel)
            .filter(
                IdeaVersionModel.idea_id == idea_id,
                IdeaVersionModel.is_active.is_(True),
            )
            .first()
        )
        if model is None:
            return None
        return self._to_entity(model)

    def deactivate_active_versions(self, idea_id: str) -> None:
        active_models = (
            self.db.query(IdeaVersionModel)
            .filter(
                IdeaVersionModel.idea_id == idea_id,
                IdeaVersionModel.is_active.is_(True),
            )
            .all()
        )

        for model in active_models:
            model.is_active = False
            model.status = VersionStatus.DERIVED.value
            model.updated_at = datetime.now(timezone.utc).isoformat()

        self.db.commit()

    def activate_version(self, version_id: str) -> IdeaVersion | None:
        model = (
            self.db.query(IdeaVersionModel)
            .filter(IdeaVersionModel.id == version_id)
            .first()
        )

        if model is None:
            return None

        model.is_active = True
        model.status = VersionStatus.ACTIVE.value
        model.updated_at = datetime.now(timezone.utc).isoformat()

        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def _to_entity(self, model: IdeaVersionModel) -> IdeaVersion:
        return IdeaVersion(
            id=model.id,
            idea_id=model.idea_id,
            source_variant_id=model.source_variant_id,
            parent_version_id=model.parent_version_id,
            content=model.content,
            version_number=model.version_number,
            transformation_type=TransformationType(model.transformation_type),
            user_instruction=model.user_instruction,
            is_active=model.is_active,
            status=VersionStatus(model.status),
            created_at=datetime.fromisoformat(model.created_at),
            updated_at=datetime.fromisoformat(model.updated_at),
        )