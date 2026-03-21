from pydantic import BaseModel, Field


class IdeaCreateRequest(BaseModel):
    """Request contract for registering a new idea inside a session."""

    session_id: str = Field(..., min_length=1, description="Parent session ID")
    initial_prompt: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="User's initial idea input",
    )


class IdeaCreateResponse(BaseModel):
    """Response returned after creating a new idea."""

    idea_id: str = Field(..., description="Unique idea identifier")
    session_id: str = Field(..., description="Parent session ID")
    initial_prompt: str = Field(..., description="Original user input")
    message: str = Field(..., description="Operation result message")