from pathlib import Path

from fastapi import APIRouter, HTTPException  # type: ignore[import-not-found]

from app.schemas.repository import RepositoryCreate, RepositoryResponse
from app.services.git_service import GitService
from app.services.code_indexer import CodeIndexer
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore


router = APIRouter(
    prefix="/repositories",
    tags=["repositories"],
)

git_service = GitService()
code_indexer = CodeIndexer()
chunking_service = ChunkingService()
embedding_service = EmbeddingService()
vector_store = VectorStore()


@router.post(
    "/",
    response_model=RepositoryResponse,
    summary="Clone and index a GitHub repository",
    description=(
        "Clone a public GitHub repository, discover its source files, "
        "create code chunks, generate embeddings, and store them in ChromaDB."
    ),
)
async def clone_repository(
    request: RepositoryCreate,
) -> RepositoryResponse:
    """
    Clone and index a public GitHub repository.

    Flow:
        GitHub URL
            ↓
        GitService
            ↓
        CodeIndexer
            ↓
        ChunkingService
            ↓
        EmbeddingService
            ↓
        VectorStore
    """

    try:
        # 1. Clone repository
        local_path = git_service.clone_repository(
            str(request.url)
        )

        repository_name = Path(local_path).name

        # 2. Discover source-code files
        documents = code_indexer.index_repository(
            local_path
        )

        if not documents:
            raise ValueError(
                "No supported source-code files were found "
                "in the repository."
            )

        # 3. Split source files into chunks
        chunks = chunking_service.chunk_documents(
            documents
        )

        if not chunks:
            raise ValueError(
                "No code chunks could be created "
                "from the repository."
            )

        # 4. Generate embeddings
        embedded_chunks = embedding_service.embed_documents(
            chunks
        )

        # 5. Store chunks and embeddings in ChromaDB
        indexed_count = vector_store.add_documents(
            embedded_chunks
        )

        return RepositoryResponse(
            status="success",
            repository_name=repository_name,
            local_path=local_path,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to clone and index repository: {str(exc)}",
        ) from exc