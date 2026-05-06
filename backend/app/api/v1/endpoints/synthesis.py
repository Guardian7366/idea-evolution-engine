from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import get_synthesis_service
from app.application.dto.synthesis_dto import SynthesisRequest, SynthesisResponse
from app.application.services.synthesis_service import SynthesisService

router = APIRouter()


@router.get("/")
def list_syntheses():
    return {
        "message": "Synthesis endpoint is available.",
        "items": [],
    }


@router.post("/", response_model=SynthesisResponse)
def generate_synthesis(
    payload: SynthesisRequest,
    service: SynthesisService = Depends(get_synthesis_service),
) -> SynthesisResponse:
    return service.generate_synthesis(
        idea_id=payload.idea_id,
        version_id=payload.version_id,
        preferred_language=payload.language,
    )