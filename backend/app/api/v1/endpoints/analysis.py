"""Code analysis API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.code_analysis_service import CodeAnalysisService


router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
)


class AnalysisRequest(BaseModel):
    """Request payload for code analysis."""

    question: str = Field(
        ...,
        min_length=3,
        description="Question about the repository code.",
        examples=["How is age calculated from a birth date?"],
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of relevant code chunks to retrieve.",
    )


class AnalysisSource(BaseModel):
    """Source code chunk used for the AI analysis."""

    file_path: str
    language: str
    chunk_index: int
    distance: float


class AnalysisResponse(BaseModel):
    """Response payload containing the AI analysis and sources."""

    question: str
    answer: str
    sources: list[AnalysisSource]


@router.post(
    "/",
    response_model=AnalysisResponse,
    summary="Analyze repository code",
    description="Searches repository code and generates an AI-powered analysis.",
)
async def analyze_code(request: AnalysisRequest) -> AnalysisResponse:
    """Retrieve relevant code and generate an AI analysis."""

    try:
        service = CodeAnalysisService()

        result = service.analyze(
            question=request.question,
            top_k=request.top_k,
        )

        return AnalysisResponse(
            question=request.question,
            answer=result["answer"],
            sources=result["sources"],
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Code analysis failed: {str(exc)}",
        ) from exc