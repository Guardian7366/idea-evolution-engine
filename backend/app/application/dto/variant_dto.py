from pydantic import BaseModel, Field
from typing import Literal


class GenerateVariantsRequest(BaseModel):
    """Request contract for generating initial variants from an idea."""

    session_id: str = Field(..., min_length=1, description="Parent session ID")
    idea_id: str = Field(..., min_length=1, description="Parent idea ID")
    initial_prompt: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Original user idea input",
    )


class IdeaVariantItem(BaseModel):
    """Represents one generated variant option for the user."""

    variant_id: str = Field(..., description="Unique variant identifier")
    title: str = Field(..., min_length=1, description="Short variant label")
    content: str = Field(..., min_length=1, description="Variant description")
    variant_type: Literal["expansion", "focus", "creative_twist"] = Field(
        ...,
        description="Variant generation style/category",
    )


class GenerateVariantsResponse(BaseModel):
    """Response returned after generating the initial idea variants."""

    session_id: str = Field(..., description="Parent session ID")
    idea_id: str = Field(..., description="Parent idea ID")
    variants: list[IdeaVariantItem] = Field(
        ...,
        description="List of generated variants for the idea",
    )
    message: str = Field(..., description="Operation result message")