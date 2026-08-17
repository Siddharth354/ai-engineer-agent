from app.services.code_search_service import CodeSearchService
from app.services.llm_service import LLMService


class CodeAnalysisService:
    """
    Orchestrates code retrieval and LLM-based analysis.
    """

    def __init__(self):
        self.code_search_service = CodeSearchService()
        self.llm_service = LLMService()

    def analyze(
        self,
        question: str,
        top_k: int = 5,
    ) -> dict:
        """
        Search the repository for relevant code and send
        the retrieved context to the LLM.

        Returns both the AI-generated answer and the
        source code chunks used for the analysis.
        """

        search_results = self.code_search_service.search(
            query=question,
            top_k=top_k,
        )

        if not search_results:
            return {
                "answer": (
                    "I could not find relevant code in the repository "
                    "to answer this question."
                ),
                "sources": [],
            }

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

        answer = self.llm_service.analyze_code(
            question=question,
            code_context=code_context,
        )

        sources = []

        for result in search_results:
            sources.append(
                {
                    "file_path": result["file_path"],
                    "language": result["language"],
                    "chunk_index": result["chunk_index"],
                    "distance": result["distance"],
                }
            )

        return {
            "answer": answer,
            "sources": sources,
        }