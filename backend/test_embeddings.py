from app.services.code_indexer import CodeIndexer
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService


indexer = CodeIndexer()
chunker = ChunkingService()
embedder = EmbeddingService()

documents = indexer.index_repository(
    "repositories/python-mini-projects.git"
)

chunks = chunker.chunk_documents(documents)

print(f"Documents: {len(documents)}")
print(f"Chunks: {len(chunks)}")

# Test with only the first 3 chunks initially
test_chunks = chunks[:3]

embedded_chunks = embedder.embed_documents(test_chunks)

print(f"Embedded chunks: {len(embedded_chunks)}")

for chunk in embedded_chunks:
    print("\n--- EMBEDDING ---")
    print("File:", chunk["file_path"])
    print("Language:", chunk["language"])
    print("Chunk:", chunk["chunk_index"])
    print("Vector dimensions:", len(chunk["embedding"]))
    print("Vector preview:", chunk["embedding"][:5])