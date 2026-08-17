from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.code_search_service import CodeSearchService


router = APIRouter(tags=["search"])

search_service = CodeSearchService()


class SearchRequest(BaseModel):
    """Request payload for semantic code search."""

    query: str = Field(
        ...,
        min_length=1,
        description="Natural-language question or description to search for.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of relevant code chunks to return.",
    )


class SearchResult(BaseModel):
    """A single semantic code search result."""

    file_path: str
    language: str
    chunk_index: int
    distance: float
    content: str


class SearchResponse(BaseModel):
    """Semantic code search response."""

    query: str
    results: list[SearchResult]


@router.post(
    "/search",
    response_model=SearchResponse,
    summary="Search repository code",
    description="Finds code chunks relevant to a natural-language query.",
)
async def search_code(request: SearchRequest) -> SearchResponse:
    """Search indexed repository code using semantic similarity."""

    results = search_service.search(
        query=request.query,
        top_k=request.top_k,
    )

    return SearchResponse(
        query=request.query,
        results=[
            SearchResult(**result)
            for result in results
        ],
    )