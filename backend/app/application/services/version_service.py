"""
version_service.py — Servicio de aplicación para IdeaVersions.

Alineado con las entidades reales del proyecto:
- IdeaVersion: create_initial(), create_from_variant(), mark_analyzed(), mark_selected(), supersede()
- VersionRules: can_start_analysis(), can_select_variant(), can_create_next_version(), get_latest_version()
- Las versiones se guardan en su propio repositorio (VersionRepository), separado de Idea.
- La Idea real NO tiene lista de versiones — son entidades independientes.

Flujo de estados de una versión:
    DRAFT → ANALYZED → SELECTED → SUPERSEDED
"""

from typing import Optional

from app.domain.entities.idea_version import IdeaVersion
from app.domain.entities.idea_variant import IdeaVariant
from app.domain.repositories.idea_repository import IdeaRepository
from app.domain.repositories.version_repository import VersionRepository
from app.domain.rules.version_rules import VersionRules
from app.domain.value_objects.transformation_type import TransformationType


class VersionService:
    """
    Servicio que gestiona el ciclo de vida de las versiones de una idea.

    Recibe dos repositorios:
    - VersionRepository: para persistir y buscar versiones.
    - IdeaRepository: para verificar que la idea padre existe antes de crear versiones.
    """

    def __init__(
        self,
        version_repository: VersionRepository,
        idea_repository: IdeaRepository,
    ) -> None:
        self._version_repo = version_repository
        self._idea_repo = idea_repository

    # ──────────────────────────────────────────────────────────────────────────
    # CREAR VERSIONES
    # ──────────────────────────────────────────────────────────────────────────

    async def create_initial_version(
        self,
        idea_id: str,
        title: str,
        description: str,
    ) -> IdeaVersion:
        """
        Crea la primera versión (v1) de una idea recién creada.

        Usa IdeaVersion.create_initial() que genera la versión con:
        - version_number = 1
        - status = DRAFT
        - parent_version_id = None

        Si lanza "idea no encontrada": idea_service no persistió la idea
        antes de llamar este método. Revisa el orden en idea_service.create_idea().
        """
        # Verificamos que la idea padre existe.
        idea = await self._idea_repo.get_by_id(idea_id)
        if idea is None:
            raise ValueError(
                f"No se puede crear una versión: la idea '{idea_id}' no existe. "
                "Verifica que idea_service haya persistido la idea primero."
            )

        # Verificamos el límite de versiones por idea.
        existing = await self._version_repo.get_by_idea_id(idea_id)
        if not VersionRules.can_create_next_version(existing):
            raise ValueError(
                f"La idea '{idea_id}' ya tiene el máximo de versiones permitidas "
                f"({VersionRules.MAX_VERSIONS_PER_IDEA}). Genera una síntesis antes de continuar."
            )

        version = IdeaVersion.create_initial(
            idea_id=idea_id,
            title=title,
            description=description,
        )

        return await self._version_repo.save(version)

    async def create_version_from_transformation(
        self,
        idea_id: str,
        parent_version_id: str,
        selected_variant: IdeaVariant,
    ) -> IdeaVersion:
        """
        Crea una nueva versión a partir de una variante seleccionada.

        Usa IdeaVersion.create_from_variant() que:
        - Toma el contenido de la variante seleccionada como base.
        - Incrementa el version_number automáticamente.
        - Guarda referencia a la versión padre.

        También marca la versión padre como SUPERSEDED.

        Si lanza "versión padre no encontrada": el parent_version_id es incorrecto.
        """
        parent_version = await self._version_repo.get_by_id(parent_version_id)
        if parent_version is None:
            raise ValueError(
                f"La versión padre '{parent_version_id}' no existe."
            )

        existing = await self._version_repo.get_by_idea_id(idea_id)
        if not VersionRules.can_create_next_version(existing):
            raise ValueError(
                f"La idea '{idea_id}' alcanzó el máximo de versiones permitidas. "
                "Genera una síntesis final antes de seguir iterando."
            )

        # Creamos la nueva versión a partir de la variante seleccionada.
        new_version = IdeaVersion.create_from_variant(
            idea_id=idea_id,
            parent_version=parent_version,
            selected_variant=selected_variant,
        )

        # Marcamos la versión padre como SUPERSEDED — fue reemplazada.
        parent_version.supersede()
        await self._version_repo.save(parent_version)

        return await self._version_repo.save(new_version)

    # ──────────────────────────────────────────────────────────────────────────
    # OBTENER VERSIONES
    # ──────────────────────────────────────────────────────────────────────────

    async def get_version(self, idea_id: str, version_id: str) -> IdeaVersion:
        """
        Retorna una versión específica de una idea.
        Lanza ValueError si no existe.

        Recibe idea_id además de version_id para ser explícito sobre
        a qué idea pertenece la versión que buscamos.
        """
        version = await self._version_repo.get_by_id(version_id)
        if version is None or version.idea_id != idea_id:
            raise ValueError(
                f"La versión '{version_id}' no existe para la idea '{idea_id}'."
            )
        return version

    async def get_latest_version(self, idea_id: str) -> Optional[IdeaVersion]:
        """
        Retorna la versión más reciente de una idea, o None si no tiene versiones.
        Usa VersionRules.get_latest_version() para determinar cuál es la más reciente.
        """
        versions = await self._version_repo.get_by_idea_id(idea_id)
        return VersionRules.get_latest_version(versions)

    async def get_all_versions(self, idea_id: str) -> list[IdeaVersion]:
        """
        Retorna todas las versiones de una idea ordenadas por version_number.
        Usado por generate_final_synthesis para saber cuántas iteraciones hubo.
        """
        versions = await self._version_repo.get_by_idea_id(idea_id)
        return sorted(versions, key=lambda v: v.version_number)

    # ──────────────────────────────────────────────────────────────────────────
    # AVANCE DE ESTADOS
    # ──────────────────────────────────────────────────────────────────────────

    async def mark_analyzed(self, idea_id: str, version_id: str) -> IdeaVersion:
        """
        Avanza la versión de DRAFT → ANALYZED.
        Llama version.mark_analyzed() que valida la transición internamente.
        Si falla, la versión no estaba en DRAFT.
        """
        version = await self.get_version(idea_id, version_id)
        version.mark_analyzed()
        return await self._version_repo.save(version)

    async def mark_selected(self, idea_id: str, version_id: str) -> IdeaVersion:
        """
        Avanza la versión de ANALYZED → SELECTED.
        Si falla, la versión no estaba en ANALYZED todavía.
        """
        version = await self.get_version(idea_id, version_id)
        version.mark_selected()
        return await self._version_repo.save(version)

    # ──────────────────────────────────────────────────────────────────────────
    # VARIANTES
    # ──────────────────────────────────────────────────────────────────────────

    async def add_variant_to_version(
        self,
        idea_id: str,
        version_id: str,
        variant: IdeaVariant,
    ) -> IdeaVersion:
        """
        Agrega una variante generada a una versión específica.
        Después de agregar todas las variantes, se llama mark_analyzed()
        para indicar que el proceso terminó.
        """
        version = await self.get_version(idea_id, version_id)
        version.add_variant(variant)
        return await self._version_repo.save(version)

    # ──────────────────────────────────────────────────────────────────────────
    # UTILIDADES
    # ──────────────────────────────────────────────────────────────────────────

    async def assert_version_exists(self, idea_id: str, version_id: str) -> IdeaVersion:
        """
        Verifica que una versión existe y la retorna.
        Método utilitario para otros servicios que necesitan validar
        el version_id antes de operar.
        """
        return await self.get_version(idea_id, version_id)