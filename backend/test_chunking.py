from app.services.code_indexer import CodeIndexer
from app.services.chunking_service import ChunkingService


indexer = CodeIndexer()
chunker = ChunkingService()

documents = indexer.index_repository(
    "repositories/python-mini-projects.git"
)

chunks = chunker.chunk_documents(documents)

print(f"Indexed documents: {len(documents)}")
print(f"Generated chunks: {len(chunks)}")

for chunk in chunks[:5]:
    print("\n--- CHUNK ---")
    print("File:", chunk["file_path"])
    print("Language:", chunk["language"])
    print("Chunk index:", chunk["chunk_index"])
    print("Content:")
    print(chunk["content"][:500])