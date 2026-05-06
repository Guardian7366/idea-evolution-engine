from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_idea_service
from app.application.dto.idea_dto import IdeaCreateRequest, IdeaResponse
from app.application.dto.variant_dto import VariantListResponse
from app.application.services.idea_service import IdeaService

router = APIRouter()


@router.post("/", response_model=IdeaResponse)
def create_idea(
    payload: IdeaCreateRequest,
    service: IdeaService = Depends(get_idea_service),
) -> IdeaResponse:
    return service.create_idea(payload)


@router.get("/{idea_id}", response_model=IdeaResponse)
def get_idea(
    idea_id: str,
    service: IdeaService = Depends(get_idea_service),
) -> IdeaResponse:
    idea = service.get_idea_by_id(idea_id)
    if idea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Idea not found.",
        )
    return idea


@router.post("/{idea_id}/variants", response_model=VariantListResponse)
def generate_variants(
    idea_id: str,
    language: str = Query(default="auto"),
    service: IdeaService = Depends(get_idea_service),
) -> VariantListResponse:
    return service.generate_variants(idea_id, preferred_language=language)


@router.get("/{idea_id}/variants", response_model=VariantListResponse)
def list_variants(
    idea_id: str,
    service: IdeaService = Depends(get_idea_service),
) -> VariantListResponse:
    return service.list_variants_by_idea_id(idea_id)