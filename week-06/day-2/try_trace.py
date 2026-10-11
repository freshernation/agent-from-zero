"""Read what your agent actually did. Run from the repo root:

    python3 week-06/day-2/try_trace.py

Needs AGENT_PROVIDER set to claude or openai in .env.
"""

from agent import run_agent
from kit import SCHEMAS, TOOLS
from llm import connect
from show import format_trace, summary

TASK = (
    "I pay 1450 rent, 60 for the phone and 85 for electricity each month. "
    "Save each of those as its own note, then tell me the yearly total."
)

model = connect()
print(f"Provider: {model.name}\nTask: {TASK}\n")

result = run_agent(model, TASK, SCHEMAS, TOOLS,
                   system="You are Desk. Use your tools; do not do arithmetic yourself.")
print(format_trace(result["trace"]))
print(f"\n{summary(result)}")
