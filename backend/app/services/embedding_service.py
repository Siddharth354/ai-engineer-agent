from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Generates vector embeddings for code chunks using
    a local open-source embedding model.
    """

    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self):
        self.model = SentenceTransformer(self.MODEL_NAME)

    def embed_text(self, text: str) -> list[float]:
        """
        Generate an embedding for a single piece of text.
        """
        if not text.strip():
            raise ValueError("Cannot generate embedding for empty text.")

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_documents(
        self,
        documents: list[dict],
    ) -> list[dict]:
        """
        Generate embeddings for multiple documents.
        """

        if not documents:
            return []

        texts = [document["content"] for document in documents]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        results = []

        for document, embedding in zip(documents, embeddings):
            results.append(
                {
                    **document,
                    "embedding": embedding.tolist(),
                }
            )

        return results