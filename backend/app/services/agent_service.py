from app.services.code_search_service import CodeSearchService
from app.services.llm_service import LLMService
from app.services.intent_service import IntentService


class AgentService:
    """
    AI Engineer Agent that performs repository-level analysis.

    The agent:
    1. Understands the user's intent.
    2. Searches the repository for relevant code.
    3. Builds repository context.
    4. Sends the context and question to the LLM.
    """

    def __init__(self):
        self.code_search_service = CodeSearchService()
        self.llm_service = LLMService()
        self.intent_service = IntentService()

    def analyze_repository(
        self,
        question: str,
        top_k: int = 8,
    ) -> str:
        """
        Analyze the repository and answer the user's question.
        """

        # ---------------------------------------------------------
        # 1. Validate question
        # ---------------------------------------------------------

        if not question.strip():
            return "Please provide a question or task."

        # ---------------------------------------------------------
        # 2. Determine the user's engineering intent
        # ---------------------------------------------------------

        intent = self.intent_service.classify(question)

        # ---------------------------------------------------------
        # 3. Configure retrieval based on intent
        # ---------------------------------------------------------

        search_query = question
        distance_threshold = 1.2

        if intent == "REPOSITORY_OVERVIEW":
            search_query = (
                "repository structure purpose main projects "
                "application entry points important files "
                "configuration dependencies"
            )

            distance_threshold = 2.0

        elif intent == "BUG":
            search_query = question
            distance_threshold = 1.5

        elif intent == "IMPLEMENT":
            search_query = question
            distance_threshold = 1.5

        elif intent == "REFACTOR":
            search_query = question
            distance_threshold = 1.5

        elif intent == "EXPLAIN":
            search_query = question
            distance_threshold = 1.2

        # ---------------------------------------------------------
        # 4. Search repository
        # ---------------------------------------------------------

        search_results = self.code_search_service.search(
            query=search_query,
            top_k=top_k,
            distance_threshold=distance_threshold,
        )

        if not search_results:
            return (
                "I could not find enough relevant repository code "
                "to answer this question."
            )

        # ---------------------------------------------------------
        # 5. Build repository context
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # 6. Create intent-specific instructions
        # ---------------------------------------------------------

        intent_instructions = {
            "EXPLAIN": """
Explain what the existing repository code does.
Focus on the current implementation and behavior.
Do not propose changes unless the user asks for them.
""",

            "BUG": """
Investigate the user's reported problem using the retrieved code.
Identify the specific code causing the problem and explain why it
produces the observed behavior.
Clearly separate the existing behavior from the identified bug.
Do not invent code that is not present in the repository.
Do not propose a fix unless the user asks for one.
""",

            "IMPLEMENT": """
Determine what existing repository code is relevant to the requested
functionality.
Explain how the current implementation relates to the requested
feature.
If the user explicitly asks for implementation, describe the changes
required based on the retrieved code.
""",

            "REFACTOR": """
Analyze the existing implementation and identify the relevant code
that could be restructured or improved.
Explain the current structure first.
Only suggest refactoring based on code that is actually present in
the retrieved repository context.
""",

            "REPOSITORY_OVERVIEW": """
Provide a repository-level overview.
Identify the purpose, major projects, important files, technologies,
and overall structure based only on the retrieved repository code.
Do not invent files or functionality that were not retrieved.
""",
        }

        instructions = intent_instructions.get(
            intent,
            intent_instructions["EXPLAIN"],
        )

        # ---------------------------------------------------------
        # 7. Combine intent instructions with repository context
        # ---------------------------------------------------------

        final_context = f"""
Detected engineering intent:
{intent}

Intent-specific instructions:
{instructions}

Repository code context:
{repository_context}
"""

        # ---------------------------------------------------------
        # 8. Ask the LLM to analyze the repository
        # ---------------------------------------------------------

        return self.llm_service.analyze_code(
            question=question,
            code_context=final_context,
        )