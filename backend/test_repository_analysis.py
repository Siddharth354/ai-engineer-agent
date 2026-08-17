from app.services.repository_analysis_service import RepositoryAnalysisService


service = RepositoryAnalysisService()

result = service.analyze(
    question="Give me an overview of this repository and explain its main purpose.",
    top_k=10,
)

print("\n===== REPOSITORY ANALYSIS =====\n")
print(result)