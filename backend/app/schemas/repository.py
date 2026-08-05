from pydantic import BaseModel, HttpUrl


class RepositoryCreate(BaseModel):
    """
    Request model for cloning a repository.
    """
    url: HttpUrl


class RepositoryResponse(BaseModel):
    """
    Response returned after cloning.
    """
    status: str
    repository_name: str
    local_path: str