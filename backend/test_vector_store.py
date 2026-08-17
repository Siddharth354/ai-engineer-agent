from app.services.code_indexer import CodeIndexer
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore


indexer = CodeIndexer()
chunker = ChunkingService()
embedder = EmbeddingService()
vector_store = VectorStore()


# 1. Read repository
documents = indexer.index_repository(
    "repositories/python-mini-projects.git"
)

# 2. Chunk source code
chunks = chunker.chunk_documents(documents)

# 3. Generate embeddings
embedded_chunks = embedder.embed_documents(chunks)

# 4. Store everything in ChromaDB
stored = vector_store.add_documents(
    embedded_chunks
)

print(f"Indexed documents: {len(documents)}")
print(f"Generated chunks: {len(chunks)}")
print(f"Stored chunks: {stored}")
print(f"ChromaDB count: {vector_store.count()}")