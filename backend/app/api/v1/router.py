from fastapi import APIRouter

from app.api.v1.endpoints import analysis
from app.api.v1.endpoints import health
from app.api.v1.endpoints import agent
from app.api.v1.endpoints import repositories


api_router = APIRouter()

# Infrastructure
api_router.include_router(health.router)

# Repository management
api_router.include_router(repositories.router)

# AI code analysis
api_router.include_router(analysis.router)
api_router.include_router(agent.router)