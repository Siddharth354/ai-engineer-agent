from groq import Groq

from app.core.config import settings


class LLMService:
    """
    Service responsible for generating AI responses using Groq.
    """

    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)

    def analyze_code(
        self,
        question: str,
        code_context: str,
    ) -> str:
        """
        Analyze repository code using the retrieved code context.
        """

        system_prompt = """
You are GitForge AI Engineer, an AI assistant specialized in
understanding and analyzing software repositories.

Your job is to answer questions about the user's repository
using ONLY the provided repository code context.

Rules:

1. Base your answer on the retrieved repository code.
2. Do not invent files, functions, variables, or behavior.
3. Clearly mention the relevant file paths when explaining code.
4. Explain what the EXISTING code does before discussing improvements.
5. Do not rewrite or propose replacement code unless the user
   explicitly asks for a fix, refactoring, or implementation.
6. If the existing code contains a bug or incorrect logic, clearly
   state that the repository implementation is incorrect.
7. Distinguish between:
   - What the repository currently does
   - Problems or limitations in that implementation
   - Suggested improvements, only when requested
8. If the retrieved context does not contain enough information,
   say that the available repository context is insufficient.
9. Keep the answer technical but easy to understand.
"""

        user_prompt = f"""
Repository code context:

{code_context}

User question:

{question}

Answer the question based strictly on the repository context above.
"""

        response = self.client.chat.completions.create(
    model=settings.groq_model,
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ],
    temperature=0.1,
)

        return response.choices[0].message.content