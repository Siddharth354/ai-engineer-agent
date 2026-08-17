from fastapi import APIRouter

from app.api.v1.endpoints import health
from app.api.v1.endpoints import search


api_router = APIRouter()

# Infrastructure
api_router.include_router(health.router)

# Semantic code search
api_router.include_router(search.router)