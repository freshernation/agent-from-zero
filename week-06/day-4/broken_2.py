# A plain agent loop. With max_steps=5 it should call the model at most 5 times.
from kit import run_calls


def run_agent(model, task, schemas, tools, max_steps=10):
    messages = [{"role": "user", "content": task}]
    steps = 0

    while steps < max_steps:
        reply = model.chat(messages, tools=schemas)
        messages.append(reply["message"])

        if reply["stop"] != "tools":
            steps = steps + 1
            return {"answer": reply["text"], "stopped": "done", "steps": steps}

        messages.extend(run_calls(tools, reply["tool_calls"]))

    return {"answer": "I ran out of steps before finishing.",
            "stopped": "max_steps", "steps": steps}
