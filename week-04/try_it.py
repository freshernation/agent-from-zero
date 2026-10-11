"""Make one real call. Run from the repo root:

    python3 week-04/try_it.py

With AGENT_PROVIDER=fake (the default) this costs nothing and echoes you back.
Set AGENT_PROVIDER to claude or openai in .env, with the matching key, and run
it again. Do it once this week so the fake never feels like the whole story.
"""

from llm import ModelError, connect

model = connect()
print(f"Provider: {model.name}\n")

try:
    reply = model.chat(
        [{"role": "user", "content": "In one sentence, what is an AI agent?"}],
        system="You are a patient teacher. Use plain words.",
    )
except ModelError as error:
    print(f"The call failed: {error}")
else:
    print(reply["text"])
    print(f"\nstop:  {reply['stop']}")
    print(f"usage: {reply['usage']['input']} tokens in, {reply['usage']['output']} out")
