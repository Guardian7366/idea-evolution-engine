from __future__ import annotations

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.infrastructure.persistence.database import Base


class IdeaVariantModel(Base):
    __tablename__ = "idea_variants"

    id = Column(String, primary_key=True, index=True)
    idea_id = Column(String, ForeignKey("ideas.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)
    is_selected = Column(Boolean, nullable=False, default=False)
    selected_at = Column(String, nullable=True)
    created_at = Column(String, nullable=False)


class IdeaVersionModel(Base):
    __tablename__ = "idea_versions"

    id = Column(String, primary_key=True, index=True)
    idea_id = Column(String, ForeignKey("ideas.id"), nullable=False, index=True)
    source_variant_id = Column(String, ForeignKey("idea_variants.id"), nullable=True)
    parent_version_id = Column(String, ForeignKey("idea_versions.id"), nullable=True)
    content = Column(String, nullable=False)
    version_number = Column(Integer, nullable=False)
    transformation_type = Column(String, nullable=False)
    user_instruction = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=False)
    status = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)