"""
idea_service.py — Servicio de aplicación para el flujo completo de ideas.

Actualizado para usar la nueva firma de VersionService donde todos los métodos
reciben idea_id además de version_id. Esto es necesario porque la entidad Idea
real no tiene lista de versiones — las versiones son entidades independientes
que se buscan por su propio repositorio.

Cambios respecto a la versión anterior:
- create_initial_version() ahora recibe title y description (no session_id).
- get_version(), mark_analyzed(), mark_selected(), assert_version_exists()
  ahora reciben (idea_id, version_id) en lugar de solo version_id.
- get_version_history() se renombró a get_all_versions().
- select_variant() y transform_version() usan los nuevos métodos del pipeline.
"""

from typing import Optional

from app.application.dto.comparison_dto import (
    CompareVersionsRequest,
    CompareVersionsResponse,
    VersionComparisonResult,
)
from app.application.dto.idea_dto import (
    IdeaCreateRequest,
    IdeaCreateResponse,
)
from app.application.dto.perspective_dto import (
    ExplorePerspectiveRequest,
    ExplorePerspectiveResponse,
    PerspectiveAnalysisResult,
)
from app.application.dto.selection_dto import (
    SelectVariantRequest,
    SelectVariantResponse,
)
from app.application.dto.synthesis_dto import (
    FinalSynthesisResult,
    GenerateFinalSynthesisRequest,
    GenerateFinalSynthesisResponse,
)
from app.application.dto.transformation_dto import (
    TransformVersionRequest,
    TransformVersionResponse,
)
from app.application.dto.variant_dto import (
    GenerateVariantsRequest,
    GenerateVariantsResponse,
    IdeaVariantItem,
)
from app.application.dto.version_dto import ActiveIdeaVersion
from app.application.services.session_service import SessionService
from app.application.services.version_service import VersionService
from app.domain.entities.idea import Idea
from app.domain.entities.idea_variant import IdeaVariant
from app.domain.repositories.idea_repository import IdeaRepository
from app.domain.value_objects.transformation_type import TransformationType


def _build_title_from_prompt(prompt: str, max_length: int = 60) -> str:
    """
    Genera un título corto a partir del prompt del usuario.
    Toma las primeras palabras hasta el límite de caracteres.
    Si se corta, agrega "..." para indicar que hay más texto.
    """
    stripped = prompt.strip()
    if len(stripped) <= max_length:
        return stripped
    truncated = stripped[:max_length].rsplit(' ', 1)[0]
    return f"{truncated}..."


class IdeaService:
    """
    Servicio de aplicación que orquesta el flujo completo de evolución de ideas.
    """

    def __init__(
        self,
        idea_repository: IdeaRepository,
        session_service: SessionService,
        version_service: VersionService,
    ) -> None:
        self._idea_repo = idea_repository
        self._session_service = session_service
        self._version_service = version_service

    # ──────────────────────────────────────────────────────────────────────────
    # 1. CREAR IDEA
    # ──────────────────────────────────────────────────────────────────────────

    async def create_idea(self, payload: IdeaCreateRequest) -> IdeaCreateResponse:
        """
        Crea una idea nueva dentro de una sesión existente.

        Flujo:
        1. Verifica que la sesión existe y está activa.
        2. Construye el título a partir del prompt del usuario.
        3. Crea y persiste la entidad Idea.
        4. Notifica a la sesión que se agregó una idea.
        5. Crea la versión inicial (v1) de esta idea.
        6. Retorna el DTO de respuesta.
        """
        # Paso 1: Verificamos que la sesión existe y está activa.
        await self._session_service.assert_session_is_active(payload.session_id)

        # Paso 2: Generamos un título corto a partir del prompt.
        title = _build_title_from_prompt(payload.initial_prompt)

        # Paso 3: Creamos y persistimos la entidad Idea.
        idea = Idea.create(
            session_id=payload.session_id,
            title=title,
            description=payload.initial_prompt,
        )
        persisted_idea = await self._idea_repo.save(idea)

        # Paso 4: Notificamos a la sesión que tiene una idea nueva.
        await self._session_service.register_idea_added(
            payload.session_id, persisted_idea.id
        )

        # Paso 5: Creamos la versión inicial (v1) de esta idea.
        # Pasamos el título y prompt completo como title y description de la versión.
        await self._version_service.create_initial_version(
            idea_id=persisted_idea.id,
            title=title,
            description=payload.initial_prompt,
        )

        return IdeaCreateResponse(
            idea_id=persisted_idea.id,
            session_id=payload.session_id,
            initial_prompt=payload.initial_prompt,
            message="Idea created successfully",
        )

    # ──────────────────────────────────────────────────────────────────────────
    # 2. GENERAR VARIANTES
    # ──────────────────────────────────────────────────────────────────────────

    async def generate_variants(
        self,
        payload: GenerateVariantsRequest,
    ) -> GenerateVariantsResponse:
        """
        Genera variantes de una idea para que el usuario elija por dónde evolucionar.

        Estado actual: MOCK — las variantes son texto predefinido.
        Estado futuro: La IA generará variantes reales basadas en el contenido de la idea.
        """
        idea = await self._idea_repo.get_by_id(payload.idea_id)
        if idea is None:
            raise ValueError(
                f"No se pueden generar variantes: la idea '{payload.idea_id}' no existe."
            )

        # --- MOCK ---
        variants = [
            IdeaVariantItem(
                variant_id="variant_mock_001",
                title="Expanded Concept",
                content=(
                    f"An expanded version of the idea: {payload.initial_prompt} "
                    "with broader scope, more features, and clearer user value."
                ),
                variant_type="expansion",
            ),
            IdeaVariantItem(
                variant_id="variant_mock_002",
                title="Focused Direction",
                content=(
                    f"A more focused interpretation of the idea: {payload.initial_prompt} "
                    "targeted at one specific use case and a simpler execution path."
                ),
                variant_type="focus",
            ),
            IdeaVariantItem(
                variant_id="variant_mock_003",
                title="Creative Twist",
                content=(
                    f"A more original variation of the idea: {payload.initial_prompt} "
                    "with an unexpected perspective and stronger creative differentiation."
                ),
                variant_type="creative_twist",
            ),
        ]
        # --- FIN MOCK ---

        return GenerateVariantsResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            variants=variants,
            message="Variants generated successfully",
        )

    # ──────────────────────────────────────────────────────────────────────────
    # 3. SELECCIONAR VARIANTE
    # ──────────────────────────────────────────────────────────────────────────

    async def select_variant(
        self,
        payload: SelectVariantRequest,
    ) -> SelectVariantResponse:
        """
        El usuario elige una variante. Se crea la primera versión activa real.

        Flujo:
        1. Verificamos que la idea existe.
        2. Obtenemos la versión más reciente (v1 en DRAFT).
        3. Creamos la entidad IdeaVariant con la elección del usuario.
        4. Avanzamos el pipeline: DRAFT → ANALYZED → SELECTED.
        5. Retornamos el DTO con la versión activa.
        """
        idea = await self._idea_repo.get_by_id(payload.idea_id)
        if idea is None:
            raise ValueError(f"La idea '{payload.idea_id}' no existe.")

        # Obtenemos la versión más reciente (debería ser v1 en DRAFT).
        latest_version = await self._version_service.get_latest_version(payload.idea_id)
        if latest_version is None:
            raise ValueError(
                f"La idea '{payload.idea_id}' no tiene versiones. "
                "Verifica que create_idea() se ejecutó correctamente."
            )

        # Mapa de contenido de variantes mock.
        variant_content_map = {
            "variant_mock_001": ("Expanded Concept", "An expanded version of the idea with broader scope, more features, and clearer user value."),
            "variant_mock_002": ("Focused Direction", "A more focused interpretation of the idea targeted at one specific use case and a simpler execution path."),
            "variant_mock_003": ("Creative Twist", "A more original variation of the idea with an unexpected perspective and stronger creative differentiation."),
        }
        variant_title, variant_content = variant_content_map.get(
            payload.variant_id,
            ("Selected Variant", "Content generated from the selected variant.")
        )

        # Creamos la entidad IdeaVariant con la elección del usuario.
        variant = IdeaVariant.create(
            version_id=latest_version.id,
            title=variant_title,
            description=variant_content,
            transformation_type=TransformationType.SELECTION,
        )

        # Avanzamos el pipeline simplificado: DRAFT → ANALYZED → SELECTED.
        # En producción, entre DRAFT y ANALYZED habría una llamada real a la IA.
        await self._version_service.mark_analyzed(payload.idea_id, latest_version.id)
        await self._version_service.add_variant_to_version(payload.idea_id, latest_version.id, variant)
        updated_version = await self._version_service.mark_selected(payload.idea_id, latest_version.id)

        active_version = ActiveIdeaVersion(
            version_id=updated_version.id,
            idea_id=payload.idea_id,
            session_id=payload.session_id,
            title=variant_title,
            content=variant_content,
            status="active",
            version_number=updated_version.version_number,
            parent_version_id=updated_version.parent_version_id,
            source_variant_id=variant.id,
            transformation_type=TransformationType.SELECTION.value,
        )

        return SelectVariantResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            selected_variant_id=payload.variant_id,
            active_version=active_version,
            message="Variant selected and active version created successfully",
        )

    # ──────────────────────────────────────────────────────────────────────────
    # 4. TRANSFORMAR VERSIÓN
    # ──────────────────────────────────────────────────────────────────────────

    async def transform_version(
        self,
        payload: TransformVersionRequest,
    ) -> TransformVersionResponse:
        """
        El usuario pide evolucionar, refinar o mutar la versión actual.
        Crea una versión nueva a partir de la versión existente.
        """
        # Verificamos que la versión actual existe.
        current_version = await self._version_service.get_version(
            payload.idea_id, payload.version_id
        )

        # Convertimos el string del DTO al enum del dominio.
        try:
            transformation = TransformationType(payload.transformation_type)
        except ValueError:
            raise ValueError(
                f"Tipo de transformación desconocido: '{payload.transformation_type}'. "
                f"Los valores válidos son: {[t.value for t in TransformationType]}."
            )

        # Templates de contenido mock por tipo de transformación.
        transformation_templates = {
            TransformationType.EVOLVE: {
                "title_prefix": "Evolved",
                "content_suffix": "This version expands the idea into a more developed direction with additional depth, broader possibilities, and stronger structure.",
            },
            TransformationType.REFINE: {
                "title_prefix": "Refined",
                "content_suffix": "This version sharpens the core concept, improves clarity, and reduces ambiguity to make the idea more focused and practical.",
            },
            TransformationType.MUTATE: {
                "title_prefix": "Mutated",
                "content_suffix": "This version introduces a more experimental twist, changing the direction of the idea to explore a more surprising alternative.",
            },
        }
        template = transformation_templates.get(transformation, {
            "title_prefix": "Transformed",
            "content_suffix": "This version was transformed based on the given instruction.",
        })

        cleaned_instruction = payload.instruction.rstrip(". ")

        # Creamos la variante que representa el resultado de la transformación.
        transform_variant = IdeaVariant.create(
            version_id=current_version.id,
            title=f"{template['title_prefix']} Version",
            description=f"Transformation instruction: {cleaned_instruction}. {template['content_suffix']}",
            transformation_type=transformation,
        )

        # Creamos la nueva versión a partir de la variante de transformación.
        # Esto también marca la versión padre como SUPERSEDED automáticamente.
        new_version = await self._version_service.create_version_from_transformation(
            idea_id=payload.idea_id,
            parent_version_id=current_version.id,
            selected_variant=transform_variant,
        )

        # Avanzamos el pipeline de la nueva versión: DRAFT → ANALYZED → SELECTED.
        await self._version_service.mark_analyzed(payload.idea_id, new_version.id)
        updated_version = await self._version_service.mark_selected(payload.idea_id, new_version.id)

        new_active_version = ActiveIdeaVersion(
            version_id=updated_version.id,
            idea_id=payload.idea_id,
            session_id=payload.session_id,
            title=f"{template['title_prefix']} Version",
            content=f"Transformation instruction: {cleaned_instruction}. {template['content_suffix']}",
            status="active",
            version_number=updated_version.version_number,
            parent_version_id=updated_version.parent_version_id,
            source_variant_id=None,
            transformation_type=transformation.value,
        )

        return TransformVersionResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            previous_version_id=payload.version_id,
            new_active_version=new_active_version,
            message="Version transformed successfully",
        )

    # ──────────────────────────────────────────────────────────────────────────
    # 5. COMPARAR VERSIONES
    # ──────────────────────────────────────────────────────────────────────────

    async def compare_versions(
        self,
        payload: CompareVersionsRequest,
    ) -> CompareVersionsResponse:
        """
        Compara dos versiones de la misma idea.
        Estado actual: MOCK. Verificamos que ambas versiones existen antes de comparar.
        """
        await self._version_service.assert_version_exists(payload.idea_id, payload.version_id_a)
        await self._version_service.assert_version_exists(payload.idea_id, payload.version_id_b)

        # --- MOCK ---
        comparison = VersionComparisonResult(
            summary=(
                "Version A appears closer to the original direction, while Version B "
                "shows a more processed or strategically improved interpretation."
            ),
            strengths_version_a=[
                "Keeps stronger alignment with the initial concept",
                "May feel more direct and easier to understand quickly",
            ],
            strengths_version_b=[
                "Shows clearer structure and more deliberate shaping",
                "May be easier to turn into a practical MVP direction",
            ],
            key_differences=[
                "Version A is more raw or foundational",
                "Version B is more transformed and intentional",
                "Version B likely reflects stronger decision-making after iteration",
            ],
            recommendation=(
                "Use Version B as the working direction if the priority is execution clarity, "
                "but keep Version A as a reference to preserve the original creative intent."
            ),
        )
        # --- FIN MOCK ---

        return CompareVersionsResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            version_id_a=payload.version_id_a,
            version_id_b=payload.version_id_b,
            comparison=comparison,
            message="Versions compared successfully",
        )

    # ──────────────────────────────────────────────────────────────────────────
    # 6. EXPLORAR PERSPECTIVA
    # ──────────────────────────────────────────────────────────────────────────

    async def explore_perspective(
        self,
        payload: ExplorePerspectiveRequest,
    ) -> ExplorePerspectiveResponse:
        """
        Analiza la idea desde un ángulo específico.
        Estado actual: MOCK. Verificamos que la versión existe antes de analizar.
        """
        await self._version_service.assert_version_exists(payload.idea_id, payload.version_id)

        # --- MOCK ---
        perspective_templates = {
            "feasibility": PerspectiveAnalysisResult(
                perspective_type="feasibility",
                summary="This version appears reasonably viable for an MVP if the scope is kept controlled and the first implementation remains focused.",
                observations=[
                    "The concept can be reduced to a manageable first release",
                    "The core interaction seems understandable from a product standpoint",
                    "Execution risk grows if too many advanced features are added early",
                ],
                suggestion="Prioritize the minimum user flow first and postpone secondary ideas until after initial validation.",
            ),
            "innovation": PerspectiveAnalysisResult(
                perspective_type="innovation",
                summary="This version shows moderate innovation, especially if its core flow is presented in a more distinctive and memorable way.",
                observations=[
                    "The idea has familiar elements, which helps comprehension",
                    "Its novelty depends on how the evolution process is framed to users",
                    "Differentiation could increase through stronger interaction design",
                ],
                suggestion="Strengthen the most distinctive part of the user experience so the concept feels less generic and more signature-driven.",
            ),
            "user_value": PerspectiveAnalysisResult(
                perspective_type="user_value",
                summary="This version offers clear potential value if users quickly understand how it helps them move from vague ideas to clearer outcomes.",
                observations=[
                    "The main value lies in guided clarity, not raw AI output",
                    "Users may appreciate progressive assistance over one-shot generation",
                    "Perceived value improves when each step feels actionable",
                ],
                suggestion="Make the user-facing flow extremely clear so the benefit is visible from the first interaction.",
            ),
            "risks": PerspectiveAnalysisResult(
                perspective_type="risks",
                summary="The main risks are product ambiguity, feature overexpansion, and unclear differentiation if the workflow is not kept focused.",
                observations=[
                    "Too many options too early may confuse the user",
                    "The concept could become broad before proving core usefulness",
                    "Without a clear MVP boundary, execution may slow down",
                ],
                suggestion="Protect the MVP scope aggressively and validate the core loop before adding complexity.",
            ),
        }

        analysis = perspective_templates.get(payload.perspective_type)
        if analysis is None:
            raise ValueError(
                f"Tipo de perspectiva desconocido: '{payload.perspective_type}'. "
                "Los valores válidos son: feasibility, innovation, user_value, risks."
            )
        # --- FIN MOCK ---

        return ExplorePerspectiveResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            version_id=payload.version_id,
            analysis=analysis,
            message="Perspective explored successfully",
        )

    # ──────────────────────────────────────────────────────────────────────────
    # 7. GENERAR SÍNTESIS FINAL
    # ──────────────────────────────────────────────────────────────────────────

    async def generate_final_synthesis(
        self,
        payload: GenerateFinalSynthesisRequest,
    ) -> GenerateFinalSynthesisResponse:
        """
        Genera el resumen final de toda la evolución de una idea.
        Estado actual: MOCK. Verificamos que idea y versión existen antes de sintetizar.
        """
        idea = await self._idea_repo.get_by_id(payload.idea_id)
        if idea is None:
            raise ValueError(f"La idea '{payload.idea_id}' no existe.")

        await self._version_service.assert_version_exists(payload.idea_id, payload.version_id)

        # Contamos las versiones para incluirlo en la síntesis.
        version_history = await self._version_service.get_all_versions(payload.idea_id)
        total_versions = len(version_history)

        # --- MOCK ---
        synthesis = FinalSynthesisResult(
            title="Idea Evolution Engine - Final Synthesis",
            core_concept=(
                "A guided AI-powered web platform that helps users transform an "
                "initial vague idea into clearer, more structured, and more useful "
                "creative outcomes through progressive iteration."
            ),
            value_proposition=(
                "Instead of giving only one AI answer, the platform helps users "
                "explore alternatives, compare directions, refine concepts, and "
                "arrive at a stronger final idea with more clarity and control."
            ),
            recommended_next_step=(
                "Build the MVP around the simplest end-to-end loop: idea input, "
                "variant generation, variant selection, one transformation action, "
                "and a final synthesis view."
            ),
            notes=[
                f"This idea evolved through {total_versions} version(s) before synthesis.",
                "Keep the first release focused on guided clarity, not feature breadth",
                "Preserve traceability between versions and analytical outputs",
                "Use the frontend flow to make progress visible and intuitive",
            ],
        )
        # --- FIN MOCK ---

        return GenerateFinalSynthesisResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            version_id=payload.version_id,
            synthesis=synthesis,
            message="Final synthesis generated successfully",
        )