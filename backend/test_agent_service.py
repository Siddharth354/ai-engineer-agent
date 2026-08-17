from app.services.agent_service import AgentService


agent = AgentService()

question = """
What is the overall purpose of this repository?
What are the main types of projects it contains?
"""

answer = agent.analyze_repository(
    question=question,
    top_k=8,
)

print("\n===== AI ENGINEER AGENT =====\n")
print(answer)