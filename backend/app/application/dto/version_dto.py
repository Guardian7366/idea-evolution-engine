from pydantic import BaseModel, Field
from typing import Literal


class ActiveIdeaVersion(BaseModel):
    """Represents an active working version of an idea."""

    version_id: str = Field(..., description="Unique version identifier")
    idea_id: str = Field(..., description="Parent idea ID")
    session_id: str = Field(..., description="Parent session ID")
    title: str = Field(..., min_length=1, description="Short version title")
    content: str = Field(..., min_length=1, description="Main version content")
    status: Literal["active"] = Field(..., description="Current version status")
    version_number: int = Field(..., ge=1, description="Sequential version number")
    parent_version_id: str | None = Field(
        default=None,
        description="Previous version used as the source for this version",
    )
    source_variant_id: str | None = Field(
        default=None,
        description="Original selected variant if this version comes from one",
    )
    transformation_type: Literal["selection", "evolve", "refine", "mutate"] = Field(
        ...,
        description="Action that produced this version",
    )