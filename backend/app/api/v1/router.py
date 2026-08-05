"""Aggregates all API v1 route modules."""

from fastapi import APIRouter

from app.api.v1.endpoints import health,repositories

api_router = APIRouter()

# Infrastructure
api_router.include_router(health.router)
api_router.include_router(repositories.router)

# Future versioned routes:
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(repos.router, prefix="/repos", tags=["repos"])
# api_router.include_router(runs.router, prefix="/runs", tags=["runs"])
