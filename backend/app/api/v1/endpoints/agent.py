"""AI Engineer Agent API endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.agent_service import AgentService


router = APIRouter(
    prefix="/agent",
    tags=["agent"],
)


class AgentRequest(BaseModel):
    """Request payload for the AI Engineer Agent."""

    question: str = Field(
        ...,
        min_length=3,
        description="Software engineering question or task.",
        examples=[
            "What is the overall purpose of this repository?"
        ],
    )

    top_k: int = Field(
        default=8,
        ge=1,
        le=15,
        description="Number of relevant repository code chunks to retrieve.",
    )


class AgentResponse(BaseModel):
    """Response payload from the AI Engineer Agent."""

    question: str
    answer: str


@router.post(
    "/",
    response_model=AgentResponse,
    summary="Ask the AI Engineer Agent",
    description=(
        "Analyzes the repository using semantic code search "
        "and an LLM."
    ),
)
async def analyze_repository(
    request: AgentRequest,
) -> AgentResponse:
    """Analyze the repository and answer an engineering question."""

    try:
        service = AgentService()

        answer = service.analyze_repository(
            question=request.question,
            top_k=request.top_k,
        )

        return AgentResponse(
            question=request.question,
            answer=answer,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Agent analysis failed: {str(exc)}",
        ) from exc