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


class IdeaService:
    """
    Application service that orchestrates the idea flow.

    For now this service contains mock behavior only. Later, backend
    implementation can replace internals without changing API contracts.
    """

    def create_idea(self, payload: IdeaCreateRequest) -> IdeaCreateResponse:
        return IdeaCreateResponse(
            idea_id="idea_mock_001",
            session_id=payload.session_id,
            initial_prompt=payload.initial_prompt,
            message="Idea created successfully",
        )

    def generate_variants(
        self,
        payload: GenerateVariantsRequest,
    ) -> GenerateVariantsResponse:
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

        return GenerateVariantsResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            variants=variants,
            message="Variants generated successfully",
        )

    def select_variant(
        self,
        payload: SelectVariantRequest,
    ) -> SelectVariantResponse:
        selected_variant_map = {
            "variant_mock_001": {
                "title": "Expanded Concept",
                "content": (
                    "An expanded version of the idea with broader scope, "
                    "more features, and clearer user value."
                ),
            },
            "variant_mock_002": {
                "title": "Focused Direction",
                "content": (
                    "A more focused interpretation of the idea targeted at "
                    "one specific use case and a simpler execution path."
                ),
            },
            "variant_mock_003": {
                "title": "Creative Twist",
                "content": (
                    "A more original variation of the idea with an unexpected "
                    "perspective and stronger creative differentiation."
                ),
            },
        }

        selected_variant = selected_variant_map.get(
            payload.variant_id,
            {
                "title": "Selected Variant",
                "content": "Mock content generated from the selected variant.",
            },
        )

        active_version = ActiveIdeaVersion(
            version_id="version_mock_001",
            idea_id=payload.idea_id,
            session_id=payload.session_id,
            title=selected_variant["title"],
            content=selected_variant["content"],
            status="active",
            version_number=1,
            parent_version_id=None,
            source_variant_id=payload.variant_id,
            transformation_type="selection",
        )

        return SelectVariantResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            selected_variant_id=payload.variant_id,
            active_version=active_version,
            message="Variant selected and active version created successfully",
        )

    def transform_version(
        self,
        payload: TransformVersionRequest,
    ) -> TransformVersionResponse:
        cleaned_instruction = payload.instruction.rstrip(". ")

        transformation_templates = {
            "evolve": {
                "title_prefix": "Evolved",
                "content_suffix": (
                    "This version expands the idea into a more developed direction "
                    "with additional depth, broader possibilities, and stronger structure."
                ),
                "version_number": 2,
            },
            "refine": {
                "title_prefix": "Refined",
                "content_suffix": (
                    "This version sharpens the core concept, improves clarity, and "
                    "reduces ambiguity to make the idea more focused and practical."
                ),
                "version_number": 2,
            },
            "mutate": {
                "title_prefix": "Mutated",
                "content_suffix": (
                    "This version introduces a more experimental twist, changing the "
                    "direction of the idea to explore a more surprising alternative."
                ),
                "version_number": 2,
            },
        }

        selected_template = transformation_templates[payload.transformation_type]

        new_active_version = ActiveIdeaVersion(
            version_id="version_mock_002",
            idea_id=payload.idea_id,
            session_id=payload.session_id,
            title=f"{selected_template['title_prefix']} Version",
            content=(
                f"Transformation instruction: {cleaned_instruction}. "
                f"{selected_template['content_suffix']}"
            ),
            status="active",
            version_number=selected_template["version_number"],
            parent_version_id=payload.version_id,
            source_variant_id=None,
            transformation_type=payload.transformation_type,
        )

        return TransformVersionResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            previous_version_id=payload.version_id,
            new_active_version=new_active_version,
            message="Version transformed successfully",
        )

    def compare_versions(
        self,
        payload: CompareVersionsRequest,
    ) -> CompareVersionsResponse:
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

        return CompareVersionsResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            version_id_a=payload.version_id_a,
            version_id_b=payload.version_id_b,
            comparison=comparison,
            message="Versions compared successfully",
        )

    def explore_perspective(
        self,
        payload: ExplorePerspectiveRequest,
    ) -> ExplorePerspectiveResponse:
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

        analysis = perspective_templates[payload.perspective_type]

        return ExplorePerspectiveResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            version_id=payload.version_id,
            analysis=analysis,
            message="Perspective explored successfully",
        )

    def generate_final_synthesis(
        self,
        payload: GenerateFinalSynthesisRequest,
    ) -> GenerateFinalSynthesisResponse:
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
                "Keep the first release focused on guided clarity, not feature breadth",
                "Preserve traceability between versions and analytical outputs",
                "Use the frontend flow to make progress visible and intuitive",
            ],
        )

        return GenerateFinalSynthesisResponse(
            session_id=payload.session_id,
            idea_id=payload.idea_id,
            version_id=payload.version_id,
            synthesis=synthesis,
            message="Final synthesis generated successfully",
        )
