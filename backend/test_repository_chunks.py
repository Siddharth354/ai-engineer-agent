from app.services.vector_store import VectorStore


vector_store = VectorStore()

print("\n===== REPOSITORY CHUNKS =====")

print("Total chunks:", vector_store.count())

results = vector_store.get_repository_chunks(limit=20)

documents = results.get("documents", [])
metadatas = results.get("metadatas", [])

for index, (document, metadata) in enumerate(
    zip(documents, metadatas),
    start=1,
):
    print(f"\n--- Chunk {index} ---")
    print("File:", metadata["file_path"])
    print("Language:", metadata["language"])
    print("Chunk:", metadata["chunk_index"])
    print("Content:")
    print(document[:500])