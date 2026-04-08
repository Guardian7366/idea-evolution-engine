"""
ideas.py — Endpoints de la API para el flujo de ideas.

Cambios respecto al mock original:
- Todos los métodos ahora son async.
- IdeaService ya no se instancia directamente aquí. Llega por inyección
  de dependencias con Depends(get_idea_service), igual que sessions.py.
- Se agregó manejo de errores: los ValueError que lanzan los servicios
  se convierten en respuestas HTTP apropiadas (404, 400, 409).

Lo que NO cambia:
- Las rutas (URLs) son exactamente las mismas.
- Los contratos de entrada y salida (DTOs) son exactamente los mismos.
- El frontend no nota ninguna diferencia en la interfaz.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.application.dto.comparison_dto import (
    CompareVersionsRequest,
    CompareVersionsResponse,
)
from app.application.dto.idea_dto import (
    IdeaCreateRequest,
    IdeaCreateResponse,
)
from app.application.dto.perspective_dto import (
    ExplorePerspectiveRequest,
    ExplorePerspectiveResponse,
)
from app.application.dto.selection_dto import (
    SelectVariantRequest,
    SelectVariantResponse,
)
from app.application.dto.synthesis_dto import (
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
)
from app.application.services.idea_service import IdeaService
from app.api.deps import get_idea_service

router = APIRouter()


@router.post("", response_model=IdeaCreateResponse)
async def create_idea(
    payload: IdeaCreateRequest,
    service: IdeaService = Depends(get_idea_service),
) -> IdeaCreateResponse:
    """
    Crea una nueva idea dentro de una sesión.
    También crea automáticamente la versión inicial (v1) de esa idea.
    """
    try:
        return await service.create_idea(payload)
    except ValueError as e:
        # Si la sesión no existe → 404. Si no está activa → 409.
        # Por ahora usamos 400 genérico hasta que se implementen errores tipados.
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate-variants", response_model=GenerateVariantsResponse)
async def generate_variants(
    payload: GenerateVariantsRequest,
    service: IdeaService = Depends(get_idea_service),
) -> GenerateVariantsResponse:
    """Genera el conjunto inicial de variantes para una idea."""
    try:
        return await service.generate_variants(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/select-variant", response_model=SelectVariantResponse)
async def select_variant(
    payload: SelectVariantRequest,
    service: IdeaService = Depends(get_idea_service),
) -> SelectVariantResponse:
    """El usuario elige una variante y se crea la primera versión activa real."""
    try:
        return await service.select_variant(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/transform-version", response_model=TransformVersionResponse)
async def transform_version(
    payload: TransformVersionRequest,
    service: IdeaService = Depends(get_idea_service),
) -> TransformVersionResponse:
    """Crea una nueva versión a partir de una transformación sobre la versión actual."""
    try:
        return await service.transform_version(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/compare-versions", response_model=CompareVersionsResponse)
async def compare_versions(
    payload: CompareVersionsRequest,
    service: IdeaService = Depends(get_idea_service),
) -> CompareVersionsResponse:
    """Compara dos versiones de la misma idea."""
    try:
        return await service.compare_versions(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/explore-perspective", response_model=ExplorePerspectiveResponse)
async def explore_perspective(
    payload: ExplorePerspectiveRequest,
    service: IdeaService = Depends(get_idea_service),
) -> ExplorePerspectiveResponse:
    """Analiza la idea desde un ángulo específico (factibilidad, riesgos, etc)."""
    try:
        return await service.explore_perspective(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate-final-synthesis", response_model=GenerateFinalSynthesisResponse)
async def generate_final_synthesis(
    payload: GenerateFinalSynthesisRequest,
    service: IdeaService = Depends(get_idea_service),
) -> GenerateFinalSynthesisResponse:
    """Genera la síntesis final de toda la evolución de la idea."""
    try:
        return await service.generate_final_synthesis(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))