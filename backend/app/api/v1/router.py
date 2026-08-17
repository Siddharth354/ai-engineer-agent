"""Aggregates all API v1 route modules."""

from fastapi import APIRouter

from app.api.v1.endpoints import analysis
from app.api.v1.endpoints import health


api_router = APIRouter()

# Infrastructure
api_router.include_router(health.router)

# AI code analysis
api_router.include_router(analysis.router)