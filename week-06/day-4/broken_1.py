# A plain agent loop. It should handle a task that needs one tool.
from kit import run_calls


def run_agent(model, task, schemas, tools, max_steps=10):
    messages = [{"role": "user", "content": task}]
    steps = 0

    while steps < max_steps:
        reply = model.chat(messages, tools=schemas)
        steps = steps + 1

        if reply["stop"] != "tools":
            messages.append(reply["message"])
            return {"answer": reply["text"], "stopped": "done", "steps": steps}

        messages.extend(run_calls(tools, reply["tool_calls"]))
        messages.append(reply["message"])

    return {"answer": "I ran out of steps before finishing.",
            "stopped": "max_steps", "steps": steps}
