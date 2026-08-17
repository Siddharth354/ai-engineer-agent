from app.services.code_search_service import CodeSearchService
from app.services.llm_service import LLMService


class RepositoryAnalysisService:
    """
    Generates repository-level analysis using indexed repository code.
    """

    def __init__(self):
        self.code_search_service = CodeSearchService()
        self.llm_service = LLMService()

    def analyze(
        self,
        question: str,
        top_k: int = 10,
    ) -> str:

        search_results = self.code_search_service.search(
            query=question,
            top_k=top_k,
            distance_threshold=2.0,
        )

        if not search_results:
            return (
                "I could not find indexed repository code "
                "to answer this question."
            )

        context_parts = []

        for result in search_results:
            context_parts.append(
                f"""
File: {result["file_path"]}
Language: {result["language"]}
Chunk: {result["chunk_index"]}

Code:
{result["content"]}
"""
            )

        code_context = "\n".join(context_parts)

        return self.llm_service.analyze_code(
            question=question,
            code_context=code_context,
        )