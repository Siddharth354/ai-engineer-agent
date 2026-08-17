from app.services.code_indexer import CodeIndexer


indexer = CodeIndexer()

documents = indexer.index_repository(
    "repositories/python-mini-projects.git"
)

print(f"Indexed files: {len(documents)}")

for document in documents[:5]:
    print("\n--- FILE ---")
    print("Path:", document["file_path"])
    print("Language:", document["language"])
    print("Size:", document["size"])
    print("Content preview:")
    print(document["content"][:300])