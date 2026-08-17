from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore


class CodeSearchService:
    """
    Provides semantic search over indexed repository code.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def search(
        self,
        query: str,
        top_k: int = 5,
        distance_threshold: float | None = None,
    ) -> list[dict]:
        """
        Search the repository for code relevant to a natural-language query.

        If distance_threshold is provided, results above that distance
        are filtered out. Otherwise, the top_k results are returned.
        """

        if not query.strip():
            return []

        # Convert the user's query into an embedding
        query_embedding = self.embedding_service.embed_text(query)

        # Search ChromaDB
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        search_results = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            # Only apply threshold when explicitly provided
            if (
                distance_threshold is not None
                and distance > distance_threshold
            ):
                continue

            search_results.append(
                {
                    "file_path": metadata["file_path"],
                    "language": metadata["language"],
                    "chunk_index": metadata["chunk_index"],
                    "distance": distance,
                    "content": document,
                }
            )

        return search_results