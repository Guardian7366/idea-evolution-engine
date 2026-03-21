from fastapi import APIRouter

from backend.app.application.dto.comparison_dto import (
    CompareVersionsRequest,
    CompareVersionsResponse,
)
from backend.app.application.dto.idea_dto import (
    IdeaCreateRequest,
    IdeaCreateResponse,
)
from backend.app.application.dto.perspective_dto import (
    ExplorePerspectiveRequest,
    ExplorePerspectiveResponse,
)
from backend.app.application.dto.selection_dto import (
    SelectVariantRequest,
    SelectVariantResponse,
)
from backend.app.application.dto.synthesis_dto import (
    GenerateFinalSynthesisRequest,
    GenerateFinalSynthesisResponse,
)
from backend.app.application.dto.transformation_dto import (
    TransformVersionRequest,
    TransformVersionResponse,
)
from backend.app.application.dto.variant_dto import (
    GenerateVariantsRequest,
    GenerateVariantsResponse,
)
from backend.app.application.services.idea_service import IdeaService

router = APIRouter()

# Service instance used by the API layer.
idea_service = IdeaService()


@router.post("", response_model=IdeaCreateResponse)
def create_idea(payload: IdeaCreateRequest) -> IdeaCreateResponse:
    """Create a new idea from the user's initial input."""
    return idea_service.create_idea(payload)


@router.post("/generate-variants", response_model=GenerateVariantsResponse)
def generate_variants(payload: GenerateVariantsRequest) -> GenerateVariantsResponse:
    """Generate the initial set of variants for one idea."""
    return idea_service.generate_variants(payload)


@router.post("/select-variant", response_model=SelectVariantResponse)
def select_variant(payload: SelectVariantRequest) -> SelectVariantResponse:
    """Select one variant and create the first active version."""
    return idea_service.select_variant(payload)


@router.post("/transform-version", response_model=TransformVersionResponse)
def transform_version(payload: TransformVersionRequest) -> TransformVersionResponse:
    """Create a new active version from the current one."""
    return idea_service.transform_version(payload)


@router.post("/compare-versions", response_model=CompareVersionsResponse)
def compare_versions(payload: CompareVersionsRequest) -> CompareVersionsResponse:
    """Compare two versions of the same idea."""
    return idea_service.compare_versions(payload)


@router.post("/explore-perspective", response_model=ExplorePerspectiveResponse)
def explore_perspective(
    payload: ExplorePerspectiveRequest,
) -> ExplorePerspectiveResponse:
    """Explore one analytical perspective over a version."""
    return idea_service.explore_perspective(payload)


@router.post(
    "/generate-final-synthesis",
    response_model=GenerateFinalSynthesisResponse,
)
def generate_final_synthesis(
    payload: GenerateFinalSynthesisRequest,
) -> GenerateFinalSynthesisResponse:
    """Generate the final synthesis for the selected version."""
    return idea_service.generate_final_synthesis(payload)