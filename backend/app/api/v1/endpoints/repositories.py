from fastapi import APIRouter, HTTPException

from app.schemas.repository import RepositoryCreate, RepositoryResponse
from app.services.git_service import GitService

router = APIRouter(prefix="/repositories", tags=["repositories"])

git_service = GitService()


@router.post("/", response_model=RepositoryResponse)
async def clone_repository(request: RepositoryCreate):
    """
    Clone a public GitHub repository.
    """
    try:
        local_path = git_service.clone_repository(str(request.url))

        return RepositoryResponse(
            status="success",
            repository_name=local_path.split("/")[-1].split("\\")[-1],
            local_path=local_path,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))