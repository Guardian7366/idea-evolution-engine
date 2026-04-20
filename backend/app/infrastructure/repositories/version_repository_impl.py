from sqlite3 import Cursor
from typing import List, Optional

from app.domain.entities.idea_version import IdeaVersion
from app.domain.repositories.version_repository import VersionRepository
from app.domain.value_objects.version_status import VersionStatus
from app.shared.database import db_wrapper


class VersionRepository(VersionRepository):
    @db_wrapper
    async def save(self, version: IdeaVersion, cursor: Cursor) -> IdeaVersion:
        """Guarda o actualiza una versión."""
        cursor.execute(
            "INSERT OR REPLACE INTO idea_versions (id, session_id, idea_id, version_number, title, content, status, is_active, source_variant_id, parent_version_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (version.id, version.session_id, version.idea_id, version.version_number, version.title, version.content, version.status.value, version.is_active, version.source_variant_id, version.parent_version_id, version.created_at.isoformat(), version.updated_at.isoformat())
        )
        return version

    @db_wrapper
    async def get_by_id(self, version_id: str, cursor: Cursor) -> Optional[IdeaVersion]:
        """Retorna la versión con ese ID o None si no existe."""
        cursor.execute("SELECT id, session_id, idea_id, version_number, title, content, status, is_active, source_variant_id, parent_version_id, created_at, updated_at FROM idea_versions WHERE id = ?", (version_id,))
        row = cursor.fetchone()
        if row:
            return IdeaVersion(
                id=row[0],
                session_id=row[1],
                idea_id=row[2],
                version_number=row[3],
                title=row[4],
                content=row[5],
                status=VersionStatus(row[6]),
                is_active=row[7],
                source_variant_id=row[8],
                parent_version_id=row[9],
                created_at=row[10],
                updated_at=row[11]
            )
        return None

    @db_wrapper
    async def get_by_idea_id(self, idea_id: str, cursor: Cursor) -> List[IdeaVersion]:
        """Retorna todas las versiones de una idea ordenadas por version_number ascendente."""
        cursor.execute("SELECT id, session_id, idea_id, version_number, title, content, status, is_active, source_variant_id, parent_version_id, created_at, updated_at FROM idea_versions WHERE idea_id = ? ORDER BY version_number ASC", (idea_id,))
        rows = cursor.fetchall()
        return [
            IdeaVersion(
                id=row[0],
                session_id=row[1],
                idea_id=row[2],
                version_number=row[3],
                title=row[4],
                content=row[5],
                status=VersionStatus(row[6]),
                is_active=row[7],
                source_variant_id=row[8],
                parent_version_id=row[9],
                created_at=row[10],
                updated_at=row[11]
            )
            for row in rows
        ]

    @db_wrapper
    async def get_latest_by_idea_id(self, idea_id: str, cursor: Cursor) -> Optional[IdeaVersion]:
        """Retorna la versión con el version_number más alto para una idea."""
        cursor.execute("SELECT id, session_id, idea_id, version_number, title, content, status, is_active, source_variant_id, parent_version_id, created_at, updated_at FROM idea_versions WHERE idea_id = ? ORDER BY version_number DESC LIMIT 1", (idea_id,))
        row = cursor.fetchone()
        if row:
            return IdeaVersion(
                id=row[0],
                session_id=row[1],
                idea_id=row[2],
                version_number=row[3],
                title=row[4],
                content=row[5],
                status=VersionStatus(row[6]),
                is_active=row[7],
                source_variant_id=row[8],
                parent_version_id=row[9],
                created_at=row[10],
                updated_at=row[11]
            )
        return None

    @db_wrapper
    async def get_by_status(self, session_id: str, status: VersionStatus, cursor: Cursor) -> List[IdeaVersion]:
        """Retorna todas las ideas versionadas con un estado específico."""
        cursor.execute("SELECT id, session_id, idea_id, version_number, title, content, status, is_active, source_variant_id, parent_version_id, created_at, updated_at FROM idea_versions WHERE session_id = ? AND status = ?", (session_id, status.value))
        rows = cursor.fetchall()
        return [
            IdeaVersion(
                id=row[0],
                session_id=row[1],
                idea_id=row[2],
                version_number=row[3],
                title=row[4],
                content=row[5],
                status=VersionStatus(row[6]),
                is_active=row[7],
                source_variant_id=row[8],
                parent_version_id=row[9],
                created_at=row[10],
                updated_at=row[11]
            )
            for row in rows
        ]


    @db_wrapper
    async def get_next_version_number(self, idea_id: str, cursor: Cursor) -> int:
        """Calcula el próximo número de versión para una idea."""
        cursor.execute("SELECT COALESCE(MAX(version_number), 0) + 1 FROM idea_versions WHERE idea_id = ?", (idea_id,))
        row = cursor.fetchone()
        return row[0] if row else 1

    @db_wrapper
    async def delete(self, version_id: str, cursor: Cursor) -> bool:
        """Elimina una versión. Retorna True si se eliminó, False si no existía."""
        cursor.execute("DELETE FROM idea_versions WHERE id = ?", (version_id,))
        return cursor.rowcount > 0
