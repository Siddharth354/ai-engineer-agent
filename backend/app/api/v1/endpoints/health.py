"""Health check endpoint for load balancers and monitoring."""

from pydantic import BaseModel, Field

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Health check response payload."""

    status: str = Field(
    default="ok",
    description="Current service health status"
)
    app_name: str
    version: str
    environment: str


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns service health status. Used by load balancers and monitoring.",
)
async def health_check() -> HealthResponse:
    """Verify the API is running and report basic service metadata."""
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )
