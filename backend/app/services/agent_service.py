from app.services.code_search_service import CodeSearchService
from app.services.llm_service import LLMService


class AgentService:
    """
    AI Engineer Agent that analyzes repository code
    using semantic search and an LLM.
    """

    def __init__(self):
        self.code_search_service = CodeSearchService()
        self.llm_service = LLMService()

    def analyze_repository(
        self,
        question: str,
        top_k: int = 8,
    ) -> str:
        """
        Analyze the repository and answer a developer question.
        """

        if not question.strip():
            return "Please provide a question."

        # Step 1: Search repository
        search_results = self.code_search_service.search(
            query=question,
            top_k=top_k,
        )

        if not search_results:
            return (
                "I could not find enough relevant repository code "
                "to answer this question."
            )

        # Step 2: Build repository context
        context_parts = []

        for result in search_results:
            context_parts.append(
                f"""
File: {result["file_path"]}
Language: {result["language"]}
Chunk: {result["chunk_index"]}
Distance: {result["distance"]}

Code:
{result["content"]}
"""
            )

        repository_context = "\n".join(context_parts)

        # Step 3: Ask LLM to analyze repository
        return self.llm_service.analyze_code(
            question=question,
            code_context=repository_context,
        )