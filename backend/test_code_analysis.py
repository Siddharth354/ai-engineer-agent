from app.services.code_analysis_service import CodeAnalysisService


service = CodeAnalysisService()

question = "How is age calculated from a birth date?"

answer = service.analyze(
    question=question,
    top_k=5,
)

print("\n===== CODE ANALYSIS =====")
print(f"Question: {question}")
print("\n===== AI ANSWER =====")
print(answer)