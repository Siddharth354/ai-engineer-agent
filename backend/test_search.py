from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore


embedder = EmbeddingService()
vector_store = VectorStore()

query = "calculate age from birth date"

query_embedding = embedder.embed_text(query)

results = vector_store.search(
    query_embedding=query_embedding,
    top_k=5,
)

print("\n===== SEARCH RESULTS =====")

documents = results.get("documents", [[]])[0]
metadatas = results.get("metadatas", [[]])[0]
distances = results.get("distances", [[]])[0]

for index, (document, metadata, distance) in enumerate(
    zip(documents, metadatas, distances),
    start=1,
):
    print(f"\n--- Result {index} ---")
    print("File:", metadata["file_path"])
    print("Language:", metadata["language"])
    print("Chunk:", metadata["chunk_index"])
    print("Distance:", distance)
    print("Content:")
    print(document[:500])