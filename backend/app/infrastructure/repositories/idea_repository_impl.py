from sqlite3 import Cursor
from typing import List, Optional

from app.domain.entities.idea import Idea
from app.domain.repositories.idea_repository import IdeaRepository


class IdeaRepository(IdeaRepository):
    async def save(self, idea: Idea, cursor: Cursor) -> Idea:
        """Guarda o actualiza una idea."""
        cursor.execute(
            "INSERT OR REPLACE INTO ideas (id, session_id, title, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (idea.id, idea.session_id, idea.title, idea.content, idea.created_at.isoformat(), idea.updated_at.isoformat())
        )
        return idea

    async def get_by_id(self, idea_id: str, cursor: Cursor) -> Optional[Idea]:
        """Retorna la idea con ese ID o None si no existe."""
        cursor.execute("SELECT id, session_id, title, content, created_at, updated_at FROM ideas WHERE id = ?", (idea_id,))
        row = cursor.fetchone()
        if row:
            return Idea(
                id=row[0],
                session_id=row[1],
                title=row[2],
                content=row[3],
                created_at=row[4],
                updated_at=row[5]
            )
        return None

    async def get_by_session_id(self, session_id: str, cursor: Cursor) -> List[Idea]:
        """Retorna todas las ideas de una sesión."""
        cursor.execute("SELECT id, session_id, title, content, created_at, updated_at FROM ideas WHERE session_id = ?", (session_id,))
        rows = cursor.fetchall()
        return [
            Idea(
                id=row[0],
                session_id=row[1],
                title=row[2],
                content=row[3],
                created_at=row[4],
                updated_at=row[5]
            )
            for row in rows
        ]

    async def get_active_by_session_id(self, session_id: str, cursor: Cursor) -> List[Idea]:
        """Retorna las ideas de una sesión (el esquema actual no incluye is_archived)."""
        cursor.execute("SELECT id, session_id, title, content, created_at, updated_at FROM ideas WHERE session_id = ?", (session_id,))
        rows = cursor.fetchall()
        return [
            Idea(
                id=row[0],
                session_id=row[1],
                title=row[2],
                content=row[3],
                created_at=row[4],
                updated_at=row[5]
            )
            for row in rows
        ]

    async def delete(self, idea_id: str, cursor: Cursor) -> bool:
        """Elimina una idea. Retorna True si se eliminó, False si no existía."""
        cursor.execute("DELETE FROM ideas WHERE id = ?", (idea_id,))
        return cursor.rowcount > 0

    async def exists(self, idea_id: str, cursor: Cursor) -> bool:
        """Verifica si una idea existe sin cargarla completa."""
        cursor.execute("SELECT 1 FROM ideas WHERE id = ?", (idea_id,))
        return cursor.fetchone() is not None
