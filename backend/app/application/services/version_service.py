"""
version_service.py — Servicio de aplicación para IdeaVersions.

¿Qué orquesta este servicio?
- La creación de versiones a partir de ideas existentes.
- El avance del pipeline de estados: DRAFT → ANALYZING → ANALYZED → SELECTED → SYNTHESIZED.
- La selección de variantes por parte del usuario.
- La creación de nuevas versiones a partir de una transformación (evolve, refine, mutate).

Relación con otros servicios:
- Depende de SessionService para validar que la sesión esté activa antes de operar.
- Es consumido por los endpoints de ideas.py (select-variant, transform-version).
- Cuando idea_service.py esté completo, lo llamará para crear versiones iniciales.

Relación con el dominio:
- Usa IdeaVersion (entidad), VersionRules y VariantRules (reglas de negocio).
- Usa VersionRepository e IdeaRepository para persistencia.
- No conoce nada de FastAPI, Pydantic ni HTTP.
"""

from typing import Optional

from app.domain.entities.idea_version import IdeaVersion
from app.domain.entities.idea_variant import IdeaVariant
from app.domain.repositories.version_repository import VersionRepository
from app.domain.repositories.idea_repository import IdeaRepository
from app.domain.rules.version_rules import VersionRules
from app.domain.rules.variant_rules import VariantRules
from app.domain.value_objects.version_status import VersionStatus
from app.domain.value_objects.transformation_type import TransformationType


class VersionService:
    """
    Servicio de aplicación para el ciclo de vida de IdeaVersions y IdeaVariants.

    Recibe los repositorios por inyección de dependencias.
    Cuando la BD real esté lista, solo cambia la implementación
    del repositorio en deps.py — este servicio no necesita cambios.

    ¿Por qué recibe IdeaRepository además de VersionRepository?
    Porque antes de crear una versión necesita verificar que la idea
    padre existe. Sin acceso al repositorio de ideas, tendría que
    confiar ciegamente en el idea_id recibido.
    """

    def __init__(
        self,
        version_repository: VersionRepository,
        idea_repository: IdeaRepository,
    ) -> None:
        self._version_repo = version_repository
        self._idea_repo = idea_repository

    # ──────────────────────────────────────────────────────────────────────────
    # CREAR VERSIÓN
    # ──────────────────────────────────────────────────────────────────────────

    async def create_initial_version(
        self,
        idea_id: str,
        session_id: str,
    ) -> IdeaVersion:
        """
        Crea la primera versión (v1) de una idea recién creada.

        ¿Quién llama este método?
        idea_service.py justo después de crear una Idea exitosamente.
        La versión inicial representa el estado original de la idea
        antes de cualquier transformación.

        Flujo:
        1. Verifica que la idea existe.
        2. Verifica que no se supera el límite de versiones (aunque para v1 siempre pasa).
        3. Crea la IdeaVersion en estado DRAFT.
        4. Persiste y retorna.

        Si lanza "idea no encontrada", idea_service no persistió la idea
        antes de llamar este método. Revisa el orden de operaciones en idea_service.py.
        """
        # Verificamos que la idea padre existe antes de crear su versión.
        idea = await self._idea_repo.get_by_id(idea_id)
        if idea is None:
            raise ValueError(
                f"No se puede crear una versión para la idea '{idea_id}' "
                "porque no existe. Verifica que idea_service.py haya persistido "
                "la idea antes de llamar create_initial_version()."
            )

        # Verificamos el límite de versiones por idea (MAX_VERSIONS_PER_IDEA = 10).
        existing_count = len(await self._version_repo.get_by_idea_id(idea_id))
        VersionRules.assert_can_create_new_version(existing_count)

        # Calculamos el número de versión siguiente de forma segura.
        # get_next_version_number() evita colisiones si hay concurrencia.
        version_number = await self._version_repo.get_next_version_number(idea_id)

        # IdeaVersion.create() es el factory method. Nace siempre en DRAFT.
        version = IdeaVersion.create(
            idea_id=idea_id,
            session_id=session_id,
            version_number=version_number,
            parent_version_id=None,  # v1 no tiene padre
        )

        return await self._version_repo.save(version)

    async def create_version_from_transformation(
        self,
        idea_id: str,
        session_id: str,
        parent_version_id: str,
        transformation_type: TransformationType,
    ) -> IdeaVersion:
        """
        Crea una nueva versión a partir de una transformación sobre la versión actual.

        ¿Cuándo se llama?
        Cuando el usuario elige "evolve", "refine" o "mutate" sobre una versión existente.
        Corresponde al endpoint POST /ideas/transform-version en ideas.py.

        Parámetros:
        - parent_version_id: La versión sobre la que se aplica la transformación.
          Debe existir y estar en estado SELECTED (el usuario ya eligió una variante).
        - transformation_type: El tipo de transformación (EVOLVE, REFINE o MUTATE).
          SELECTION no aplica aquí — esa transformación la maneja select_variant().

        Si lanza "versión no puede sintetizarse", la versión padre no está en SELECTED.
        El usuario debe seleccionar una variante antes de transformar.
        """
        # Verificamos que la versión padre existe.
        parent_version = await self._version_repo.get_by_id(parent_version_id)
        if parent_version is None:
            raise ValueError(
                f"La versión padre '{parent_version_id}' no existe. "
                "Verifica que el parent_version_id sea correcto."
            )

        # La versión padre debe estar en SELECTED para poder derivar una nueva.
        VersionRules.assert_can_synthesize(parent_version)

        # Verificamos el límite de versiones por idea.
        existing_count = len(await self._version_repo.get_by_idea_id(idea_id))
        VersionRules.assert_can_create_new_version(existing_count)

        version_number = await self._version_repo.get_next_version_number(idea_id)

        version = IdeaVersion.create(
            idea_id=idea_id,
            session_id=session_id,
            version_number=version_number,
            parent_version_id=parent_version_id,
        )

        return await self._version_repo.save(version)

    # ──────────────────────────────────────────────────────────────────────────
    # OBTENER VERSIONES
    # ──────────────────────────────────────────────────────────────────────────

    async def get_version(self, version_id: str) -> IdeaVersion:
        """
        Retorna una versión por su ID.
        Lanza ValueError si no existe — el endpoint lo convierte en HTTP 404.
        """
        version = await self._version_repo.get_by_id(version_id)
        if version is None:
            raise ValueError(
                f"Versión '{version_id}' no encontrada. "
                "Verifica que el version_id sea correcto."
            )
        return version

    async def get_versions_for_idea(self, idea_id: str) -> list[IdeaVersion]:
        """
        Retorna todas las versiones de una idea ordenadas por version_number ascendente.
        Útil para mostrar el historial evolutivo completo de una idea.
        """
        return await self._version_repo.get_by_idea_id(idea_id)

    async def get_latest_version(self, idea_id: str) -> Optional[IdeaVersion]:
        """
        Retorna la versión más reciente de una idea, o None si no tiene versiones.
        Usado para continuar el flujo desde el último estado conocido.
        """
        return await self._version_repo.get_latest_by_idea_id(idea_id)

    # ──────────────────────────────────────────────────────────────────────────
    # AVANCE DE ESTADOS
    # ──────────────────────────────────────────────────────────────────────────

    async def start_analysis(self, version_id: str) -> IdeaVersion:
        """
        Avanza la versión de DRAFT → ANALYZING.

        ¿Quién llama este método?
        analysis_service.py justo antes de enviar la versión a la IA para análisis.
        Marca que el proceso de análisis comenzó y previene llamadas duplicadas a la IA.

        Si lanza error, la versión no está en DRAFT.
        Probablemente ya fue enviada a analizar anteriormente.
        """
        version = await self.get_version(version_id)
        VersionRules.assert_can_start_analysis(version)

        # advance_status() valida la transición internamente usando VersionStatus.
        version.advance_status(VersionStatus.ANALYZING)
        return await self._version_repo.save(version)

    async def mark_analysis_complete(self, version_id: str) -> IdeaVersion:
        """
        Avanza la versión de ANALYZING → ANALYZED.

        ¿Quién llama este método?
        analysis_service.py después de que la IA terminó de generar variantes
        y el VersionAnalysis fue persistido exitosamente.

        Si lanza error aquí pero el análisis ya se guardó, hay una inconsistencia
        de estado. Revisar el manejo de errores en analysis_service.py para
        asegurar que este método siempre se llame si el análisis fue exitoso.
        """
        version = await self.get_version(version_id)
        version.advance_status(VersionStatus.ANALYZED)
        return await self._version_repo.save(version)

    # ──────────────────────────────────────────────────────────────────────────
    # SELECCIÓN DE VARIANTE
    # ──────────────────────────────────────────────────────────────────────────

    async def select_variant(
        self,
        version_id: str,
        variant_id: str,
        existing_variants: list[IdeaVariant],
    ) -> IdeaVersion:
        """
        Registra la variante elegida por el usuario y avanza la versión a SELECTED.

        Corresponde al endpoint POST /ideas/select-variant en ideas.py.

        Parámetros:
        - version_id: La versión sobre la que se hace la selección.
        - variant_id: La variante elegida por el usuario.
        - existing_variants: Lista de todas las variantes de esta versión.
          El servicio que llama (o el endpoint) debe cargarlas previamente.
          Se pasan aquí para que VariantRules valide que no hay otra ya seleccionada.

        Flujo:
        1. Carga la versión.
        2. Valida con VersionRules que la versión está en ANALYZED.
        3. Valida con VariantRules que la selección es válida (no hay otra seleccionada).
        4. Llama mark_variant_selected() en la entidad, que avanza a SELECTED.
        5. Persiste y retorna.

        Si lanza "versión no está en ANALYZED": la IA no terminó el análisis todavía.
        Si lanza "ya hay una variante seleccionada": el endpoint se llamó dos veces.
        """
        version = await self.get_version(version_id)

        # Validamos que la versión puede recibir una selección.
        VersionRules.assert_can_select_variant(version)

        # Buscamos la variante específica en la lista recibida.
        variant = next((v for v in existing_variants if v.id == variant_id), None)
        if variant is None:
            raise ValueError(
                f"La variante '{variant_id}' no pertenece a la versión '{version_id}'. "
                "Verifica que variant_id y version_id correspondan a la misma versión."
            )

        # Validamos con VariantRules que la selección es única en esta versión.
        VariantRules.assert_can_select(variant, existing_variants)

        # mark_variant_selected() registra la variante Y avanza el estado a SELECTED.
        version.mark_variant_selected(variant_id)

        return await self._version_repo.save(version)

    # ──────────────────────────────────────────────────────────────────────────
    # UTILIDADES PARA OTROS SERVICIOS
    # ──────────────────────────────────────────────────────────────────────────

    async def assert_version_exists(self, version_id: str) -> IdeaVersion:
        """
        Verifica que una versión existe y la retorna.
        Método utilitario para que analysis_service y synthesis_service
        validen el version_id antes de operar sobre él.
        """
        return await self.get_version(version_id)

    async def get_version_history(self, idea_id: str) -> list[IdeaVersion]:
        """
        Retorna el historial completo de versiones de una idea
        ordenado de la más antigua a la más reciente.

        Usado por synthesis_service para construir el contexto evolutivo
        que se le pasa a la IA al generar la síntesis final.
        """
        return await self._version_repo.get_by_idea_id(idea_id)