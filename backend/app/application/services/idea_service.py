"""
idea_service.py — Servicio de aplicación para el flujo completo de ideas.

¿Qué hace este servicio?
Es el cerebro principal del proyecto. Coordina todo el flujo de evolución:
desde que el usuario escribe su primera idea, hasta que obtiene una síntesis final.

Piénsalo como el director de orquesta: no toca ningún instrumento directamente,
pero sabe en qué orden debe entrar cada uno y se asegura de que todo suene bien.

¿Qué operaciones maneja?
1. create_idea         → El usuario escribe su idea inicial.
2. generate_variants   → Se generan variantes de la idea (mock por ahora, IA después).
3. select_variant      → El usuario elige una variante y se crea la primera versión real.
4. transform_version   → El usuario pide evolucionar, refinar o mutar la versión actual.
5. compare_versions    → Se comparan dos versiones para ver cuál es mejor.
6. explore_perspective → Se analiza la idea desde un ángulo específico (riesgos, valor, etc).
7. generate_final_synthesis → Se genera el resumen final de toda la evolución.

¿Qué operaciones son reales vs mock?
- create_idea, select_variant y transform_version: ya usan el dominio real.
- generate_variants, compare_versions, explore_perspective y generate_final_synthesis:
  siguen siendo mock por ahora. Cuando la IA esté integrada, se reemplaza
  el interior de esos métodos sin cambiar nada más.

Regla importante: este servicio NUNCA retorna entidades del dominio directamente.
Siempre retorna DTOs (los objetos de app/application/dto/) porque eso es lo que
espera la API. La transformación de entidad → DTO ocurre dentro de cada método.
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

    Como el usuario solo escribe un prompt libre (ej: "una app para encontrar
    compañeros de viaje"), tomamos las primeras palabras hasta llenar el límite
    de caracteres y le agregamos "..." si se cortó.

    Esto cubre el hecho de que nuestra entidad Idea requiere un título,
    pero el DTO del frontend solo envía initial_prompt.

    Si en el futuro el frontend envía un título explícito, se puede
    reemplazar esta función por simplemente usar ese título.
    """
    stripped = prompt.strip()
    if len(stripped) <= max_length:
        return stripped
    # Cortamos en el último espacio antes del límite para no cortar palabras a la mitad
    truncated = stripped[:max_length].rsplit(' ', 1)[0]
    return f"{truncated}..."


class IdeaService:
    """
    Servicio de aplicación que orquesta el flujo completo de evolución de ideas.

    Recibe sus dependencias por inyección (repositorio de ideas, servicio de sesiones,
    servicio de versiones). Esto permite que en tests se puedan usar mocks sin
    tocar este archivo.

    ¿Cómo se conecta con FastAPI?
    En deps.py se agrega una función get_idea_service() que instancia este servicio
    con los repositorios y servicios correctos. El endpoint en ideas.py usará
    Depends(get_idea_service) para recibirlo automáticamente.
    """

    def __init__(
        self,
        idea_repository: IdeaRepository,
        session_service: SessionService,
        version_service: VersionService,
    ) -> None:
        # Repositorio para persistir y buscar ideas.
        self._idea_repo = idea_repository

        # Usamos SessionService para verificar que la sesión existe y está activa
        # antes de crear una idea. También para notificarle cuando se agrega una idea.
        self._session_service = session_service

        # Usamos VersionService para crear la versión inicial de cada idea
        # y para gestionar las transformaciones posteriores.
        self._version_service = version_service

    # ──────────────────────────────────────────────────────────────────────────
    # 1. CREAR IDEA
    # ──────────────────────────────────────────────────────────────────────────

    async def create_idea(self, payload: IdeaCreateRequest) -> IdeaCreateResponse:
        """
        Crea una idea nueva dentro de una sesión existente.

        Flujo completo:
        1. Verifica que la sesión existe y está activa.
           Si no está activa, no se pueden agregar ideas.
        2. Construye el título a partir del prompt del usuario.
        3. Crea la entidad Idea con el factory method Idea.create().
        4. La persiste en el repositorio.
        5. Le notifica a la sesión que se agregó una idea (actualiza su contador).
        6. Crea la versión inicial (v1) de esta idea via VersionService.
        7. Retorna el DTO de respuesta que espera el frontend.

        Si falla en el paso 1: la sesión no existe o no está en estado ACTIVE.
        Si falla en el paso 6: version_service no pudo crear la versión inicial.
          Revisa que la idea haya sido persistida correctamente antes de ese paso.
        """
        # Paso 1: Verificamos que la sesión existe y está activa.
        # Si la sesión está pausada, archivada o no existe, esto lanza un ValueError
        # que el endpoint convierte en HTTP 404 o 409 según el caso.
        await self._session_service.assert_session_is_active(payload.session_id)

        # Paso 2: Generamos un título corto a partir del prompt libre del usuario.
        title = _build_title_from_prompt(payload.initial_prompt)

        # Paso 3: Creamos la entidad Idea.
        # Idea.create() es el factory method que genera el UUID, timestamps
        # y garantiza que la idea nazca en un estado válido.
        # El prompt completo se guarda como description para no perder nada.
        idea = Idea.create(
            session_id=payload.session_id,
            title=title,
            description=payload.initial_prompt,
        )

        # Paso 4: Persistimos la idea en el repositorio (mock en memoria por ahora).
        persisted_idea = await self._idea_repo.save(idea)

        # Paso 5: Notificamos a la sesión que tiene una idea nueva.
        # Esto actualiza el contador total_ideas en la sesión.
        # Si esto falla, la sesión cambió de estado entre el paso 1 y este punto
        # (muy raro, pero posible en entornos concurrentes).
        await self._session_service.register_idea_added(payload.session_id)

        # Paso 6: Creamos la versión inicial (v1) de esta idea.
        # Toda idea nace con su primera versión en estado DRAFT.
        # Esta versión es la base sobre la que se generarán variantes después.
        await self._version_service.create_initial_version(
            idea_id=persisted_idea.id,
            session_id=payload.session_id,
        )

        # Paso 7: Retornamos el DTO que espera el frontend.
        # El contrato no cambia respecto al mock anterior:
        # sigue retornando idea_id, session_id, initial_prompt y message.
        # La diferencia es que ahora idea_id es un UUID real, no "idea_mock_001".
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

        Antes de generar, verificamos que la idea realmente existe.
        Esto evita generar variantes para ideas que no están en el sistema.

        Cuando la IA esté integrada, el interior de este método cambiará
        pero el contrato de entrada/salida (payload → response) se mantiene igual.
        """
        # Verificamos que la idea existe antes de generar variantes para ella.
        # Si no existe, lanzamos un error claro en lugar de generar variantes huérfanas.
        idea = await self._idea_repo.get_by_id(payload.idea_id)
        if idea is None:
            raise ValueError(
                f"No se pueden generar variantes: la idea '{payload.idea_id}' no existe. "
                "Asegúrate de haber creado la idea antes de pedir variantes."
            )

        # --- MOCK: lógica temporal hasta que la IA esté integrada ---
        # Estas variantes son respuestas predefinidas que simulan lo que haría la IA.
        # Cuando se integre la IA real, se reemplaza este bloque por la llamada
        # al cliente de IA en infrastructure/ai/clients/llm_client.py.
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
        El usuario elige una variante. Con esa elección se crea la primera versión
        activa real de la idea.

        Flujo:
        1. Verificamos que la idea existe.
        2. Obtenemos la versión inicial (v1) de la idea, que está en DRAFT.
        3. Creamos una entidad IdeaVariant real con la variante seleccionada.
        4. La persistimos y marcamos como seleccionada en la versión.
        5. Avanzamos la versión a través del pipeline: DRAFT → ANALYZING → ANALYZED → SELECTED.
           (De forma simplificada por ahora, sin pasar por la IA real.)
        6. Retornamos el DTO con la versión activa.

        Nota sobre el pipeline simplificado:
        En producción, entre ANALYZING y ANALYZED habría una llamada a la IA.
        Por ahora avanzamos directamente para que el flujo funcione end-to-end.
        Cuando la IA esté lista, se agrega esa llamada entre esos dos pasos.
        """
        # Paso 1: Verificamos que la idea existe.
        idea = await self._idea_repo.get_by_id(payload.idea_id)
        if idea is None:
            raise ValueError(
                f"La idea '{payload.idea_id}' no existe. "
                "No se puede seleccionar una variante sin una idea válida."
            )

        # Paso 2: Obtenemos la versión más reciente de la idea.
        # Normalmente en este punto solo existe v1 en estado DRAFT.
        latest_version = await self._version_service.get_latest_version(payload.idea_id)
        if latest_version is None:
            raise ValueError(
                f"La idea '{payload.idea_id}' no tiene versiones. "
                "Esto no debería ocurrir si create_idea funcionó correctamente. "
                "Verifica que create_initial_version() se haya ejecutado."
            )

        # Mapa de variantes mock disponibles.
        # Cuando la IA esté integrada, las variantes vendrán del repositorio
        # en lugar de este diccionario hardcodeado.
        variant_content_map = {
            "variant_mock_001": ("Expanded Concept", "An expanded version of the idea with broader scope, more features, and clearer user value."),
            "variant_mock_002": ("Focused Direction", "A more focused interpretation of the idea targeted at one specific use case and a simpler execution path."),
            "variant_mock_003": ("Creative Twist", "A more original variation of the idea with an unexpected perspective and stronger creative differentiation."),
        }

        # Obtenemos el contenido de la variante seleccionada.
        # Si el variant_id no está en el mapa (ej: variante custom), usamos un fallback.
        variant_title, variant_content = variant_content_map.get(
            payload.variant_id,
            ("Selected Variant", "Content generated from the selected variant.")
        )

        # Paso 3: Creamos una entidad IdeaVariant real con la selección del usuario.
        variant = IdeaVariant.create(
            version_id=latest_version.id,
            idea_id=payload.idea_id,
            title=variant_title,
            description=variant_content,
            transformation_type=TransformationType.SELECTION,
            transformation_rationale="Variante seleccionada por el usuario del conjunto inicial.",
            ai_generated=False,  # Por ahora es mock, no generada por IA real
        )

        # Paso 4: Avanzamos el pipeline de la versión de forma simplificada.
        # DRAFT → ANALYZING → ANALYZED: simulamos que la IA analizó la versión.
        # En producción, entre estos dos pasos habría una llamada real a la IA.
        await self._version_service.start_analysis(latest_version.id)
        await self._version_service.mark_analysis_complete(latest_version.id)

        # ANALYZED → SELECTED: registramos la variante elegida.
        # Pasamos la variante en una lista porque select_variant necesita
        # verificar que no haya otra variante ya seleccionada en esta versión.
        updated_version = await self._version_service.select_variant(
            version_id=latest_version.id,
            variant_id=variant.id,
            existing_variants=[variant],
        )

        # Paso 5: Construimos el DTO de la versión activa que espera el frontend.
        # Mapeamos nuestra entidad IdeaVersion + IdeaVariant → ActiveIdeaVersion DTO.
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
        Esto crea una versión nueva a partir de la versión existente.

        Flujo:
        1. Verificamos que la versión actual existe.
        2. Convertimos el tipo de transformación del DTO al tipo del dominio.
        3. Creamos una nueva versión usando VersionService.
        4. Avanzamos el pipeline de la nueva versión de forma simplificada.
        5. Retornamos el DTO con la nueva versión activa.

        Igual que en select_variant, el pipeline se avanza de forma simplificada
        hasta que la IA real esté integrada.
        """
        # Paso 1: Verificamos que la versión sobre la que se transforma existe.
        current_version = await self._version_service.get_version(payload.version_id)

        # Paso 2: Convertimos el string del DTO ("evolve", "refine", "mutate")
        # al enum del dominio (TransformationType.EVOLVE, etc.).
        # Si llega un valor desconocido, TransformationType lanzará un error claro.
        try:
            transformation = TransformationType(payload.transformation_type)
        except ValueError:
            raise ValueError(
                f"Tipo de transformación desconocido: '{payload.transformation_type}'. "
                f"Los valores válidos son: {[t.value for t in TransformationType]}."
            )

        # Templates de contenido según el tipo de transformación.
        # Igual que generate_variants, esto es mock hasta que la IA esté lista.
        transformation_templates = {
            TransformationType.EVOLVE: {
                "title_prefix": "Evolved",
                "content_suffix": (
                    "This version expands the idea into a more developed direction "
                    "with additional depth, broader possibilities, and stronger structure."
                ),
            },
            TransformationType.REFINE: {
                "title_prefix": "Refined",
                "content_suffix": (
                    "This version sharpens the core concept, improves clarity, and "
                    "reduces ambiguity to make the idea more focused and practical."
                ),
            },
            TransformationType.MUTATE: {
                "title_prefix": "Mutated",
                "content_suffix": (
                    "This version introduces a more experimental twist, changing the "
                    "direction of the idea to explore a more surprising alternative."
                ),
            },
        }

        template = transformation_templates.get(transformation, {
            "title_prefix": "Transformed",
            "content_suffix": "This version was transformed based on the given instruction.",
        })

        cleaned_instruction = payload.instruction.rstrip(". ")

        # Paso 3: Creamos la nueva versión usando VersionService.
        # Esto valida que la versión padre esté en SELECTED y que no se supere
        # el límite de versiones por idea (MAX_VERSIONS_PER_IDEA = 10).
        new_version = await self._version_service.create_version_from_transformation(
            idea_id=payload.idea_id,
            session_id=payload.session_id,
            parent_version_id=current_version.id,
            transformation_type=transformation,
        )

        # Paso 4: Avanzamos el pipeline de la nueva versión de forma simplificada.
        # DRAFT → ANALYZING → ANALYZED: simulamos análisis de IA.
        await self._version_service.start_analysis(new_version.id)
        await self._version_service.mark_analysis_complete(new_version.id)

        # Creamos una variante que representa el resultado de la transformación
        # y la seleccionamos automáticamente (no hay opciones en transform, es directo).
        transform_variant = IdeaVariant.create(
            version_id=new_version.id,
            idea_id=payload.idea_id,
            title=f"{template['title_prefix']} Version",
            description=f"Transformation instruction: {cleaned_instruction}. {template['content_suffix']}",
            transformation_type=transformation,
            transformation_rationale=f"Transformación aplicada por el usuario: {payload.instruction}",
            ai_generated=False,
        )

        # ANALYZED → SELECTED: seleccionamos la variante de transformación.
        updated_version = await self._version_service.select_variant(
            version_id=new_version.id,
            variant_id=transform_variant.id,
            existing_variants=[transform_variant],
        )

        # Paso 5: Construimos el DTO de la nueva versión activa.
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

        Estado actual: MOCK — el análisis comparativo es texto predefinido.
        Estado futuro: La IA generará un análisis real basado en el contenido de ambas versiones.

        Sí verificamos que ambas versiones existen antes de "compararlas",
        para no devolver una comparación sobre versiones fantasma.
        """
        # Verificamos que ambas versiones existen antes de compararlas.
        await self._version_service.assert_version_exists(payload.version_id_a)
        await self._version_service.assert_version_exists(payload.version_id_b)

        # --- MOCK: análisis comparativo predefinido ---
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
        Analiza la idea desde un ángulo específico: factibilidad, innovación,
        valor para el usuario o riesgos.

        Estado actual: MOCK — los análisis son plantillas predefinidas.
        Estado futuro: La IA generará un análisis real basado en el contenido
        de la versión y el tipo de perspectiva solicitada.

        Verificamos que la versión existe antes de analizarla.
        """
        # Verificamos que la versión que se quiere analizar existe.
        await self._version_service.assert_version_exists(payload.version_id)

        # --- MOCK: plantillas de análisis por tipo de perspectiva ---
        perspective_templates = {
            "feasibility": PerspectiveAnalysisResult(
                perspective_type="feasibility",
                summary=(
                    "This version appears reasonably viable for an MVP if the scope "
                    "is kept controlled and the first implementation remains focused."
                ),
                observations=[
                    "The concept can be reduced to a manageable first release",
                    "The core interaction seems understandable from a product standpoint",
                    "Execution risk grows if too many advanced features are added early",
                ],
                suggestion=(
                    "Prioritize the minimum user flow first and postpone secondary ideas "
                    "until after initial validation."
                ),
            ),
            "innovation": PerspectiveAnalysisResult(
                perspective_type="innovation",
                summary=(
                    "This version shows moderate innovation, especially if its core flow "
                    "is presented in a more distinctive and memorable way."
                ),
                observations=[
                    "The idea has familiar elements, which helps comprehension",
                    "Its novelty depends on how the evolution process is framed to users",
                    "Differentiation could increase through stronger interaction design",
                ],
                suggestion=(
                    "Strengthen the most distinctive part of the user experience so the "
                    "concept feels less generic and more signature-driven."
                ),
            ),
            "user_value": PerspectiveAnalysisResult(
                perspective_type="user_value",
                summary=(
                    "This version offers clear potential value if users quickly understand "
                    "how it helps them move from vague ideas to clearer outcomes."
                ),
                observations=[
                    "The main value lies in guided clarity, not raw AI output",
                    "Users may appreciate progressive assistance over one-shot generation",
                    "Perceived value improves when each step feels actionable",
                ],
                suggestion=(
                    "Make the user-facing flow extremely clear so the benefit is visible "
                    "from the first interaction."
                ),
            ),
            "risks": PerspectiveAnalysisResult(
                perspective_type="risks",
                summary=(
                    "The main risks are product ambiguity, feature overexpansion, and "
                    "unclear differentiation if the workflow is not kept focused."
                ),
                observations=[
                    "Too many options too early may confuse the user",
                    "The concept could become broad before proving core usefulness",
                    "Without a clear MVP boundary, execution may slow down",
                ],
                suggestion=(
                    "Protect the MVP scope aggressively and validate the core loop before "
                    "adding complexity."
                ),
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
        Es el último paso del flujo: el usuario obtiene un documento consolidado
        con el resultado de todo el proceso.

        Estado actual: MOCK — la síntesis es texto predefinido.
        Estado futuro: La IA generará una síntesis real basada en todo el historial
        de versiones, variantes y análisis de la idea.

        Verificamos que la idea y la versión existen antes de sintetizar.
        """
        # Verificamos que la idea existe.
        idea = await self._idea_repo.get_by_id(payload.idea_id)
        if idea is None:
            raise ValueError(
                f"La idea '{payload.idea_id}' no existe. "
                "No se puede generar una síntesis sin una idea válida."
            )

        # Verificamos que la versión sobre la que se sintetiza existe.
        await self._version_service.assert_version_exists(payload.version_id)

        # Obtenemos el historial de versiones para saber cuántas iteraciones hubo.
        # Aunque por ahora no lo usamos en el mock, estará disponible cuando
        # la IA real necesite este contexto para generar la síntesis.
        version_history = await self._version_service.get_version_history(payload.idea_id)
        total_versions = len(version_history)

        # --- MOCK: síntesis predefinida ---
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