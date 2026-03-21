from pydantic import BaseModel, Field


class GenerateFinalSynthesisRequest(BaseModel):
    """Request contract for generating the final synthesis of an idea."""

    session_id: str = Field(..., min_length=1, description="Parent session ID")
    idea_id: str = Field(..., min_length=1, description="Parent idea ID")
    version_id: str = Field(..., min_length=1, description="Base version ID for synthesis")


class FinalSynthesisResult(BaseModel):
    """Represents the final structured synthesis of the idea."""

    title: str = Field(..., description="Final synthesized idea title")
    core_concept: str = Field(..., description="Main idea summary")
    value_proposition: str = Field(..., description="Main value delivered to the user")
    recommended_next_step: str = Field(
        ...,
        description="Most recommended next step after synthesis",
    )
    notes: list[str] = Field(
        ...,
        description="Complementary notes that summarize important considerations",
    )


class GenerateFinalSynthesisResponse(BaseModel):
    """Response returned after generating the final synthesis."""

    session_id: str = Field(..., description="Parent session ID")
    idea_id: str = Field(..., description="Parent idea ID")
    version_id: str = Field(..., description="Base version used for synthesis")
    synthesis: FinalSynthesisResult = Field(
        ...,
        description="Final synthesized result",
    )
    message: str = Field(..., description="Operation result message")