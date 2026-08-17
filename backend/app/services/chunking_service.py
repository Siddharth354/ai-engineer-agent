from typing import Any


class ChunkingService:
    """
    Service responsible for splitting source-code documents into
    smaller chunks suitable for embedding and retrieval.
    """

    DEFAULT_CHUNK_SIZE = 1500
    DEFAULT_OVERLAP = 200

    def __init__(
        self,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        overlap: int = DEFAULT_OVERLAP,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if overlap < 0:
            raise ValueError("overlap cannot be negative")

        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_documents(
        self,
        documents: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Split indexed documents into smaller chunks.

        Each chunk preserves the original file path and language.
        """

        chunks: list[dict[str, Any]] = []

        for document in documents:
            content = document.get("content", "")

            if not content.strip():
                continue

            file_path = document.get("file_path", "")
            language = document.get("language", "")

            document_chunks = self._chunk_text(content)

            for chunk_index, chunk_content in enumerate(document_chunks):
                chunks.append(
                    {
                        "file_path": file_path,
                        "language": language,
                        "chunk_index": chunk_index,
                        "content": chunk_content,
                    }
                )

        return chunks

    def _chunk_text(self, text: str) -> list[str]:
        """
        Split text into overlapping chunks.

        This is the initial implementation. We will later replace
        this with code-aware Tree-sitter chunking.
        """

        if not text.strip():
            return []

        chunks: list[str] = []

        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + self.chunk_size, text_length)

            chunk = text[start:end]

            if chunk.strip():
                chunks.append(chunk)

            if end >= text_length:
                break

            start = end - self.overlap

        return chunks