from app.services.agent_service import AgentService


print("\n===== AI ENGINEER AGENT =====\n")

question = input("Enter your question: ")

agent = AgentService()

answer = agent.analyze_repository(
    question=question,
    top_k=8,
)

print("\n===== ANSWER =====\n")
print(answer)