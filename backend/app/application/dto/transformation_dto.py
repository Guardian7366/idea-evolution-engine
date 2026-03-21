from pydantic import BaseModel, Field
from typing import Literal

from backend.app.application.dto.version_dto import ActiveIdeaVersion


class TransformVersionRequest(BaseModel):
    """Request contract for transforming the current active version."""

    session_id: str = Field(..., min_length=1, description="Parent session ID")
    idea_id: str = Field(..., min_length=1, description="Parent idea ID")
    version_id: str = Field(..., min_length=1, description="Current active version ID")
    transformation_type: Literal["evolve", "refine", "mutate"] = Field(
        ...,
        description="Type of transformation to apply",
    )
    instruction: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="User instruction guiding the transformation",
    )


class TransformVersionResponse(BaseModel):
    """Response returned after creating a transformed version."""

    session_id: str = Field(..., description="Parent session ID")
    idea_id: str = Field(..., description="Parent idea ID")
    previous_version_id: str = Field(..., description="Source version ID")
    new_active_version: ActiveIdeaVersion = Field(
        ...,
        description="New active version created from the transformation",
    )
    message: str = Field(..., description="Operation result message")