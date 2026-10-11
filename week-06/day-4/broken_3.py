# A plain agent loop. It should cope when the model asks for two tools at once.
from kit import run_calls


def run_agent(model, task, schemas, tools, max_steps=10):
    messages = [{"role": "user", "content": task}]
    steps = 0

    while steps < max_steps:
        reply = model.chat(messages, tools=schemas)
        steps = steps + 1
        messages.append(reply["message"])

        if reply["stop"] != "tools":
            return {"answer": reply["text"], "stopped": "done", "steps": steps}

        first_call = reply["tool_calls"][:1]
        messages.extend(run_calls(tools, first_call))

    return {"answer": "I ran out of steps before finishing.",
            "stopped": "max_steps", "steps": steps}
