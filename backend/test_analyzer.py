from app.services.analyzer_service import AnalyzerService


service = AnalyzerService()
result = service.analyze_repository(
    "repositories/Hello-World.git"
)
print(result)