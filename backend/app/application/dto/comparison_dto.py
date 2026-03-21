from pydantic import BaseModel, Field


class CompareVersionsRequest(BaseModel):
    """Request contract for comparing two versions of the same idea."""

    session_id: str = Field(..., min_length=1, description="Parent session ID")
    idea_id: str = Field(..., min_length=1, description="Parent idea ID")
    version_id_a: str = Field(..., min_length=1, description="First version ID")
    version_id_b: str = Field(..., min_length=1, description="Second version ID")


class VersionComparisonResult(BaseModel):
    """Represents the analytical comparison between two idea versions."""

    summary: str = Field(..., description="High-level comparison summary")
    strengths_version_a: list[str] = Field(
        ...,
        description="Main strengths detected in version A",
    )
    strengths_version_b: list[str] = Field(
        ...,
        description="Main strengths detected in version B",
    )
    key_differences: list[str] = Field(
        ...,
        description="Main differences between both versions",
    )
    recommendation: str = Field(
        ...,
        description="Suggested next decision based on the comparison",
    )


class CompareVersionsResponse(BaseModel):
    """Response returned after comparing two versions."""

    session_id: str = Field(..., description="Parent session ID")
    idea_id: str = Field(..., description="Parent idea ID")
    version_id_a: str = Field(..., description="First compared version ID")
    version_id_b: str = Field(..., description="Second compared version ID")
    comparison: VersionComparisonResult = Field(
        ...,
        description="Comparison result for both versions",
    )
    message: str = Field(..., description="Operation result message")