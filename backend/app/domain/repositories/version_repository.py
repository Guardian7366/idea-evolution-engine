"""
version_repository.py — Contrato abstracto para la persistencia de IdeaVersions.

CAMBIOS TAREA 5 (Alineación con persistencia real):

1. Este contrato ya estaba bastante bien alineado con la implementación.
   El único ajuste fue documentar mejor cada método con notas sobre
   cómo la implementación SQLite los resuelve, para que Backend 1
   tenga contexto claro al revisar o modificar la impl.

2. get_next_version_number() ya está en la impl usando COALESCE(MAX, 0) + 1.
   Se documenta explícitamente para que quede claro cómo funciona y
   por qué es preferible a calcular el máximo en memoria desde el servicio.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.idea_version import IdeaVersion
from app.domain.value_objects.version_status import VersionStatus


class VersionRepository(ABC):
    """
    Contrato abstracto para la persistencia de IdeaVersions.
    Cualquier implementación debe respetar exactamente estos métodos y firmas.
    """

    @abstractmethod
    async def save(self, version: IdeaVersion) -> IdeaVersion:
        """
        Persiste una versión nueva o actualiza una existente.
        La implementación SQLite usa INSERT OR REPLACE, por lo que
        save() funciona tanto para crear como para actualizar.
        """
        ...

    @abstractmethod
    async def get_by_id(self, version_id: str) -> Optional[IdeaVersion]:
        """Retorna una versión por su ID, o None si no existe."""
        ...

    @abstractmethod
    async def get_by_idea_id(self, idea_id: str) -> List[IdeaVersion]:
        """
        Retorna todas las versiones de una idea ordenadas por version_number ASC.
        No incluye las variantes de cada versión — esas se cargan por separado
        cuando se necesitan (lazy loading implícito).
        """
        ...

    @abstractmethod
    async def get_latest_by_idea_id(self, idea_id: str) -> Optional[IdeaVersion]:
        """
        Retorna la versión con el version_number más alto para una idea.
        La implementación SQLite usa ORDER BY version_number DESC LIMIT 1,
        más eficiente que traer todas y calcular el máximo en memoria.
        Retorna None si la idea no tiene versiones todavía.
        """
        ...

    @abstractmethod
    async def get_by_status(
        self, session_id: str, status: VersionStatus
    ) -> List[IdeaVersion]:
        """
        Retorna versiones de una sesión filtradas por estado.
        Útil para consultas como "todas las versiones SELECTED de esta sesión"
        sin traer el historial completo.
        """
        ...

    @abstractmethod
    async def get_next_version_number(self, idea_id: str) -> int:
        """
        Calcula el próximo número de versión para una idea de forma segura.

        La implementación SQLite usa:
            SELECT COALESCE(MAX(version_number), 0) + 1 FROM idea_versions WHERE idea_id = ?

        Esto garantiza que:
        - Si no hay versiones previas, retorna 1.
        - Si hay versiones, retorna el siguiente número en la secuencia.
        - Evita colisiones en entornos con múltiples requests concurrentes.

        Preferible a calcular el máximo en memoria desde el servicio porque
        la query se ejecuta como operación atómica en la BD.
        """
        ...

    @abstractmethod
    async def delete(self, version_id: str) -> bool:
        """
        Elimina una versión por su ID.
        Retorna True si existía y fue eliminada, False si no existía.
        """
        ...