import chromadb


class VectorStore:
    """
    Local ChromaDB vector store for repository code chunks.
    """

    COLLECTION_NAME = "code_chunks"

    def __init__(self, persist_directory: str = "chroma_db"):
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={
                "description": "GitForge AI Engineer code chunks"
            },
        )

    def add_documents(
        self,
        documents: list[dict],
    ) -> int:
        """
        Store code chunks and their embeddings in ChromaDB.
        """

        if not documents:
            return 0

        ids = []
        embeddings = []
        documents_text = []
        metadatas = []

        for index, document in enumerate(documents):
            file_path = document["file_path"]
            chunk_index = document["chunk_index"]

            document_id = f"{file_path}:{chunk_index}"

            ids.append(document_id)

            embeddings.append(document["embedding"])

            documents_text.append(
                document["content"]
            )

            metadatas.append(
                {
                    "file_path": file_path,
                    "language": document["language"],
                    "chunk_index": chunk_index,
                }
            )

        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents_text,
            metadatas=metadatas,
        )

        return len(documents)

    def count(self) -> int:
        """Return the number of stored code chunks."""
        return self.collection.count()

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> dict:
        """
        Search for the most relevant code chunks.
        """

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )