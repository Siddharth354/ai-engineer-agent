from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.groq_api_key)

models = client.models.list()

print("\n===== AVAILABLE GROQ MODELS =====\n")

for model in models.data:
    print(model.id)