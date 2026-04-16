from pydantic import BaseModel, Field

from app.application.dto.version_dto import ActiveIdeaVersion


class SelectVariantRequest(BaseModel):
    """Request contract for selecting an initial variant."""

    session_id: str = Field(..., min_length=1, description="Parent session ID")
    idea_id: str = Field(..., min_length=1, description="Parent idea ID")
    variant_id: str = Field(..., min_length=1, description="Selected variant ID")
    variant_title: str = Field(..., min_length=1, description="Title of the selected variant")
    variant_content: str = Field(..., min_length=1, description="Content of the selected variant")


class SelectVariantResponse(BaseModel):
    """Response returned after selecting a variant and activating a version."""

    session_id: str = Field(..., description="Parent session ID")
    idea_id: str = Field(..., description="Parent idea ID")
    selected_variant_id: str = Field(..., description="Chosen variant ID")
    active_version: ActiveIdeaVersion = Field(
        ...,
        description="New active version created from the selected variant",
    )
    message: str = Field(..., description="Operation result message")
