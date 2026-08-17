from groq import Groq

from app.core.config import settings


class LLMService:
    """
    Service responsible for interacting with the LLM.
    """

    def __init__(self):
        if not settings.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured. "
                "Add it to the backend .env file."
            )

        self.client = Groq(
            api_key=settings.groq_api_key
        )

        self.model = settings.groq_model

    def analyze_code(
        self,
        question: str,
        code_context: str,
    ) -> str:
        """
        Analyze retrieved repository code and answer the user's question.
        """

        system_prompt = """
You are GitForge AI Engineer, an AI software engineering assistant.

You analyze source code from a repository and answer questions
using the provided code context.

Rules:
1. Base your answer primarily on the provided code.
2. Do not invent files, functions, or behavior that are not present.
3. Explain your reasoning clearly.
4. Mention relevant file paths when useful.
5. If the provided context is insufficient, say so.
"""

        user_prompt = f"""
User question:
{question}

Repository code context:
{code_context}

Analyze the provided code and answer the user's question.
"""

        response = self.client.chat.completions.create(
            model=self.model,
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
            temperature=0.2,
        )

        return response.choices[0].message.content or ""