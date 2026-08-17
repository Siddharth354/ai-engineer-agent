from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Generates vector embeddings for repository code
    using a local open-source embedding model.
    """

    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self):
        self.model = SentenceTransformer(self.MODEL_NAME)

    def embed_text(self, text: str) -> list[float]:
        """
        Generate an embedding for a single piece of text.
        """

        if not text or not text.strip():
            raise ValueError(
                "Cannot generate embedding for empty text."
            )

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

        return embedding.tolist()

    def embed_documents(
        self,
        documents: list[dict],
    ) -> list[dict]:
        """
        Generate embeddings for multiple repository
        code chunks in a single batch.
        """

        if not documents:
            return []

        texts = [
            document["content"]
            for document in documents
            if document.get("content", "").strip()
        ]

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=True,
            batch_size=32,
        )

        results = []

        embedding_index = 0

        for document in documents:
            content = document.get("content", "")

            if not content.strip():
                continue

            results.append(
                {
                    **document,
                    "embedding": embeddings[
                        embedding_index
                    ].tolist(),
                }
            )

            embedding_index += 1

        return results