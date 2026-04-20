from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

@dataclass
class Idea:
    """
    Entidad raíz del dominio. Representa una idea en su estado más puro,
    sin versiones ni variantes aún — solo el concepto central del usuario.
    """
    id: str
    session_id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    is_archived: bool = False

    @classmethod
    def create(cls, session_id: str, title: str, content: str) -> "Idea":
        """Factory method. Único punto de creación de una idea nueva."""
        now = datetime.now(timezone.utc)
        return cls(
            id=str(uuid4()),
            session_id=session_id,
            title=title,
            content=content,
            created_at=now,
            updated_at=now,
        )

    def update_content(self, title: Optional[str] = None, content: Optional[str] = None) -> None:
        """
        Actualiza el contenido de la idea.

        IMPORTANTE:
        No se permite modificar una idea archivada.
        """
        self.ensure_editable()

        self.title = title if title is not None else self.title
        self.content = content if content is not None else self.content
        self.updated_at = datetime.now(timezone.utc)

    def archive(self) -> None:
        """Archiva la idea. Una idea archivada no puede editarse."""
        self.is_archived = True
        self.updated_at = datetime.now(timezone.utc)

    def ensure_editable(self) -> None:
        """Lanza excepción si la idea no puede ser modificada."""
        if self.is_archived:
            raise ValueError(f"La idea '{self.id}' está archivada y no puede modificarse.")
