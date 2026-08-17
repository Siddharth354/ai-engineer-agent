from app.services.llm_service import LLMService


llm = LLMService()

question = "How is age calculated in this repository?"

code_context = """
File: projects\\birthDateToCurrentAge.py
Language: Python

from datetime import date

def ageCalculator(years, months, days):
    age_day = 0
    age_months = 0
    age_year = 0

    today_day = int(today.strftime("%d"))
    today_month = int(today.strftime("%m"))
    today_year = int(today.strftime("%y"))

    if today_day < day:
        today_day += 31
        age_day = today_day - days
    else:
        age_day = today_day - days

    if today_month < months:
        today_month += 12
        age_months = today_month - months
    else:
        age_months = today_month - months

    age_year = today_year - years
"""

answer = llm.analyze_code(
    question=question,
    code_context=code_context,
)

print("\n===== LLM RESPONSE =====")
print(answer)