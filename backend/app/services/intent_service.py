from groq import Groq

from app.core.config import settings


class IntentService:
    """
    Determines what kind of software-engineering request
    the user is making.
    """

    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)

    def classify(self, question: str) -> str:
        """
        Classify a user request into an engineering intent.
        """

        prompt = f"""
Classify the following software engineering request into exactly
ONE of these categories:

EXPLAIN
BUG
IMPLEMENT
REFACTOR
REPOSITORY_OVERVIEW

Definitions:

EXPLAIN:
The user wants to understand existing code or behavior.

BUG:
The user wants to identify or investigate a bug or error.

IMPLEMENT:
The user wants to add new functionality.

REFACTOR:
The user wants to improve or restructure existing code.

REPOSITORY_OVERVIEW:
The user wants to understand the repository as a whole.

User request:
{question}

Return ONLY the category name.
"""

        response = self.client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )

        result = response.choices[0].message.content.strip().upper()

        valid_intents = {
            "EXPLAIN",
            "BUG",
            "IMPLEMENT",
            "REFACTOR",
            "REPOSITORY_OVERVIEW",
        }

        if result not in valid_intents:
            return "EXPLAIN"

        return result