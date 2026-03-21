from pydantic import BaseModel, Field


class SessionCreateResponse(BaseModel):
    """Response returned after creating a new session."""

    session_id: str = Field(..., description="Unique session identifier")
    message: str = Field(..., description="Operation result message")