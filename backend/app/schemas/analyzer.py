from pydantic import BaseModel, Field


class AnalyzerRequest(BaseModel):
    """Request model for repository analysis."""

    repository_path: str = Field(
        ...,
        description="Local path of the cloned repository.",
        examples=["repositories/Hello-World"],
    )


class AnalyzerResponse(BaseModel):
    """Response containing repository analysis results."""

    repository_path: str
    total_files: int
    languages: dict[str, int]
    detected_files: dict[str, bool]