from __future__ import annotations

from sqlalchemy import Column, String

from app.infrastructure.persistence.database import Base


class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=True)
    status = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)
    closed_at = Column(String, nullable=True)