from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_session_service
from app.application.dto.session_dto import SessionCreateRequest, SessionResponse
from app.application.services.session_service import SessionService

router = APIRouter()


@router.post("/", response_model=SessionResponse)
def create_session(
    payload: SessionCreateRequest,
    service: SessionService = Depends(get_session_service),
) -> SessionResponse:
    return service.create_session(payload)


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(
    session_id: str,
    service: SessionService = Depends(get_session_service),
) -> SessionResponse:
    session = service.get_session_by_id(session_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        )
    return session