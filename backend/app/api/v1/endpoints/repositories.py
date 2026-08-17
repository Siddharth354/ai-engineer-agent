from pathlib import Path

from fastapi import APIRouter, HTTPException  # type: ignore[import-not-found]

from app.schemas.repository import RepositoryCreate, RepositoryResponse
from app.services.git_service import GitService


router = APIRouter(
    prefix="/repositories",
    tags=["repositories"],
)

git_service = GitService()


@router.post(
    "/",
    response_model=RepositoryResponse,
    summary="Clone a GitHub repository",
    description="Clone a public GitHub repository and return its local path.",
)
async def clone_repository(
    request: RepositoryCreate,
) -> RepositoryResponse:
    """
    Clone a public GitHub repository.

    Args:
        request: Repository URL supplied by the client.

    Returns:
        RepositoryResponse containing clone status, repository name,
        and local path.

    Raises:
        HTTPException: If the repository cannot be cloned.
    """
    try:
        local_path = git_service.clone_repository(str(request.url))

        repository_name = Path(local_path).name

        return RepositoryResponse(
            status="success",
            repository_name=repository_name,
            local_path=local_path,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to clone repository: {str(exc)}",
        ) from exc