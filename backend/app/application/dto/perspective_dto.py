from typing import Literal

from pydantic import BaseModel, Field


class ExplorePerspectiveRequest(BaseModel):
    """Request contract for exploring one perspective over a specific version."""

    session_id: str = Field(..., min_length=1, description="Parent session ID")
    idea_id: str = Field(..., min_length=1, description="Parent idea ID")
    version_id: str = Field(..., min_length=1, description="Target version ID")
    perspective_type: Literal[
        "feasibility",
        "innovation",
        "user_value",
        "risks",
    ] = Field(
        ...,
        description="Perspective category to explore",
    )


class PerspectiveAnalysisResult(BaseModel):
    """Structured analytical result for a selected perspective."""

    perspective_type: str = Field(..., description="Applied perspective type")
    summary: str = Field(..., description="High-level result summary")
    observations: list[str] = Field(
        ...,
        description="Main perspective observations",
    )
    suggestion: str = Field(
        ...,
        description="Suggested next step based on the perspective",
    )


class ExplorePerspectiveResponse(BaseModel):
    """Response returned after exploring a perspective over a version."""

    session_id: str = Field(..., description="Parent session ID")
    idea_id: str = Field(..., description="Parent idea ID")
    version_id: str = Field(..., description="Analyzed version ID")
    analysis: PerspectiveAnalysisResult = Field(
        ...,
        description="Perspective analysis result",
    )
    message: str = Field(..., description="Operation result message")