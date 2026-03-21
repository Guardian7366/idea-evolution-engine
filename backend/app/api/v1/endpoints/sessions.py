from fastapi import APIRouter

from backend.app.application.dto.session_dto import (
    SessionCreateResponse,
)

router = APIRouter()


@router.post("", response_model=SessionCreateResponse)
def create_session() -> SessionCreateResponse:
    """
    Create a new session.

    For now this is a mock endpoint so frontend and backend
    can integrate early without waiting for persistence.
    """
    return SessionCreateResponse(
        session_id="session_mock_001",
        message="Session created successfully",
    )