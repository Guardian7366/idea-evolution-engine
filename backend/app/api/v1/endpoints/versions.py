from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import get_version_service
from app.application.dto.activation_dto import ActivateVersionRequest
from app.application.dto.selection_dto import VariantSelectionRequest
from app.application.dto.transformation_dto import TransformVersionRequest
from app.application.dto.version_dto import VersionListResponse, VersionResponse
from app.application.services.version_service import VersionService

router = APIRouter()


@router.post("/select", response_model=VersionResponse)
def select_variant(
    payload: VariantSelectionRequest,
    service: VersionService = Depends(get_version_service),
) -> VersionResponse:
    return service.create_initial_version_from_variant(payload)


@router.post("/transform", response_model=VersionResponse)
def transform_version(
    payload: TransformVersionRequest,
    service: VersionService = Depends(get_version_service),
) -> VersionResponse:
    return service.transform_version(payload)


@router.post("/activate", response_model=VersionResponse)
def activate_version(
    payload: ActivateVersionRequest,
    service: VersionService = Depends(get_version_service),
) -> VersionResponse:
    return service.activate_version(payload.version_id)


@router.get("/idea/{idea_id}", response_model=VersionListResponse)
def list_versions_by_idea(
    idea_id: str,
    service: VersionService = Depends(get_version_service),
) -> VersionListResponse:
    return service.list_versions_by_idea_id(idea_id)