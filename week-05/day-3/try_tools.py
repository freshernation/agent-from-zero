"""Watch a real model use your tools. Run from the repo root:

    python3 week-05/day-3/try_tools.py

Needs AGENT_PROVIDER set to claude or openai in .env. On the fake provider it
runs, but the fake never asks for a tool, so there is nothing to see.
"""

from llm import ModelError, connect
from round_trip import answer
from schemas import SCHEMAS

QUESTIONS = [
    "What is 4817 times 392?",
    "Please remember that the dentist is on Friday at 3pm.",
    "What is the capital of France?",
]

model = connect()
print(f"Provider: {model.name}\n")

for question in QUESTIONS:
    print(f"You:  {question}")
    try:
        print(f"Desk: {answer(model, SCHEMAS, question)}\n")
    except ModelError as error:
        print(f"The call failed: {error}\n")
