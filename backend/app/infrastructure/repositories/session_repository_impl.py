from sqlite3 import Cursor
from typing import List, Optional

from app.domain.entities.session import Session
from app.domain.repositories.session_repository import SessionRepository
from app.domain.value_objects.session_status import SessionStatus
from app.shared.database import db_wrapper


class SessionRepository(SessionRepository):
    @db_wrapper
    async def save(self, session: Session, cursor: Cursor) -> Session:
        """Guarda o actualiza una sesión."""
        cursor.execute(
            "INSERT OR REPLACE INTO sessions (id, title, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (session.id, session.title, session.status.value, session.created_at.isoformat(), session.updated_at.isoformat())
        )
        return session

    @db_wrapper
    async def get_by_id(self, session_id: str, cursor: Cursor) -> Optional[Session]:
        """Retorna la sesión con ese ID o None si no existe."""
        cursor.execute("SELECT id, title, status, created_at, updated_at FROM sessions WHERE id = ?", (session_id,))
        row = cursor.fetchone()
        if row:
            return Session(
                id=row[0],
                title=row[1],
                status=SessionStatus(row[2]),
                created_at=row[3],
                updated_at=row[4]
            )
        return None

    @db_wrapper
    async def get_all(self, limit: int, offset: int, cursor: Cursor) -> List[Session]:
        """Retorna todas las sesiones paginadas, ordenadas por created_at descendente."""
        cursor.execute("SELECT id, title, status, created_at, updated_at FROM sessions ORDER BY created_at DESC LIMIT ? OFFSET ?", (limit, offset))
        rows = cursor.fetchall()
        return [
            Session(
                id=row[0],
                title=row[1],
                status=SessionStatus(row[2]),
                created_at=row[3],
                updated_at=row[4]
            )
            for row in rows
        ]

    @db_wrapper
    async def get_by_status(self, status: SessionStatus, cursor: Cursor) -> List[Session]:
        """Retorna todas las sesiones con un estado específico."""
        cursor.execute("SELECT id, title, status, created_at, updated_at FROM sessions WHERE status = ?", (status.value,))
        rows = cursor.fetchall()
        return [
            Session(
                id=row[0],
                title=row[1],
                status=SessionStatus(row[2]),
                created_at=row[3],
                updated_at=row[4]
            )
            for row in rows
        ]

    @db_wrapper
    async def delete(self, session_id: str, cursor: Cursor) -> bool:
        """Elimina una sesión del store. Retorna True si se eliminó, False si no existía."""
        cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        return cursor.rowcount > 0

    @db_wrapper
    async def exists(self, session_id: str, cursor: Cursor) -> bool:
        """Verifica si una sesión existe sin cargarla completa."""
        cursor.execute("SELECT 1 FROM sessions WHERE id = ?", (session_id,))
        return cursor.fetchone() is not None
