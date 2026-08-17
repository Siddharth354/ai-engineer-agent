from app.services.code_search_service import CodeSearchService


search_service = CodeSearchService()

query = "calculate age from birth date"

results = search_service.search(
    query=query,
    top_k=5,
)

print("\n===== CODE SEARCH SERVICE =====")
print("Query:", query)

for index, result in enumerate(results, start=1):
    print(f"\n--- Result {index} ---")
    print("File:", result["file_path"])
    print("Language:", result["language"])
    print("Chunk:", result["chunk_index"])
    print("Distance:", result["distance"])
    print("Content:")
    print(result["content"][:500])