from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import get_analysis_service
from app.application.dto.comparison_dto import ComparisonRequest, ComparisonResponse
from app.application.dto.perspective_dto import PerspectiveRequest, PerspectiveResponse
from app.application.services.analysis_service import AnalysisService

router = APIRouter()


@router.get("/")
def list_analysis():
    return {
        "message": "Analysis endpoint is available.",
        "items": [],
    }


@router.post("/perspective", response_model=PerspectiveResponse)
def analyze_perspective(
    payload: PerspectiveRequest,
    service: AnalysisService = Depends(get_analysis_service),
) -> PerspectiveResponse:
    return service.analyze_perspective(
        version_id=payload.version_id,
        perspective=payload.perspective,
        preferred_language=payload.language,
    )


@router.post("/compare", response_model=ComparisonResponse)
def compare_versions(
    payload: ComparisonRequest,
    service: AnalysisService = Depends(get_analysis_service),
) -> ComparisonResponse:
    return service.compare_versions(
        idea_id=payload.idea_id,
        left_version_id=payload.left_version_id,
        right_version_id=payload.right_version_id,
        preferred_language=payload.language,
    )