"""Watch your agent take more than one step. Run from the repo root:

    python3 week-06/day-1/try_agent.py

Needs AGENT_PROVIDER set to claude or openai in .env. (The fake provider never
asks for a tool, so on it the agent finishes in one step.)
"""

from agent import run_agent
from kit import SCHEMAS, TOOLS
from llm import connect

TASK = "Save a note that the rent is 1450 a month, then tell me what that is per year."

model = connect()
print(f"Provider: {model.name}\nTask: {TASK}\n")

result = run_agent(model, TASK, SCHEMAS, TOOLS,
                   system="You are Desk. Use your tools; do not do arithmetic yourself.")

for message in result["messages"]:
    if message["role"] == "assistant":
        for call in message.get("tool_calls", []):
            print(f"  model asked for  {call['name']}({call['args']})")
    elif message["role"] == "tool":
        print(f"  tool returned    {message['content']}")

print(f"\nAnswer:  {result['answer']}")
print(f"Stopped: {result['stopped']} after {result['steps']} step(s)")
