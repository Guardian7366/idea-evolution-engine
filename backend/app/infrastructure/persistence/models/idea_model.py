from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String

from app.infrastructure.persistence.database import Base


class IdeaModel(Base):
    __tablename__ = "ideas"

    id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False, index=True)
    title = Column(String, nullable=True)
    content = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)