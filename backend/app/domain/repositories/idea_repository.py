"""
idea_repository.py — Contrato abstracto para la persistencia de Ideas.

El dominio depende de esta interfaz, nunca de la implementación concreta.
La implementación real vive en infrastructure/repositories/idea_repository_impl.py

CAMBIOS TAREA 5 (Alineación con persistencia real):

1. delete() ahora retorna bool en lugar de None.
   La implementación real retorna True/False según si la idea existía.
   El contrato debe reflejar eso para que los servicios puedan saber
   si la eliminación tuvo efecto.

2. Se añadió get_active_by_session_id() que ya existe en la implementación
   pero no estaba en el contrato abstracto. Sin él, la implementación tenía
   un método huérfano que el dominio no podía usar formalmente.

3. Se añadió exists() por el mismo motivo — ya existe en la impl pero
   faltaba en el contrato. Útil para validaciones rápidas sin cargar
   la entidad completa.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.idea import Idea


class IdeaRepository(ABC):
    """
    Contrato abstracto para la persistencia de Ideas.
    Cualquier implementación (SQLite, mock en memoria, PostgreSQL, etc.)
    debe respetar exactamente estos métodos y tipos de retorno.
    """

    @abstractmethod
    async def save(self, idea: Idea) -> Idea:
        """Persiste una idea nueva o actualiza una existente. Retorna la idea persistida."""
        ...

    @abstractmethod
    async def get_by_id(self, idea_id: str) -> Optional[Idea]:
        """Retorna una idea por su ID, o None si no existe."""
        ...

    @abstractmethod
    async def get_by_session_id(self, session_id: str) -> List[Idea]:
        """Retorna todas las ideas asociadas a una sesión, incluyendo archivadas."""
        ...

    @abstractmethod
    async def get_active_by_session_id(self, session_id: str) -> List[Idea]:
        """
        Retorna solo las ideas no archivadas de una sesión.

        Diferencia con get_by_session_id():
        - get_by_session_id() retorna todas, incluyendo is_archived=True.
        - Este método retorna solo las activas (is_archived=False).

        Usado cuando el frontend necesita mostrar solo ideas trabajables,
        no el historial completo de la sesión.
        """
        ...

    @abstractmethod
    async def delete(self, idea_id: str) -> bool:
        """
        Elimina una idea por su ID.

        CAMBIO: retorna bool en lugar de None.
        - True si la idea existía y fue eliminada.
        - False si no existía (operación sin efecto).

        Permite que el servicio decida si lanzar un error
        cuando se intenta eliminar algo que no existe.
        """
        ...

    @abstractmethod
    async def exists(self, idea_id: str) -> bool:
        """
        Verifica si una idea existe sin cargarla completa.

        Más eficiente que get_by_id() cuando solo necesitas saber
        si la idea existe, sin necesitar sus datos.
        Usado en validaciones previas a operaciones costosas.
        """
        ...