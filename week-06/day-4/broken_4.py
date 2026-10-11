# An agent loop with repeat detection. If the model asks for exactly the same
# call three times, the run should end with stopped == "repeating" - after
# three model calls, not ten.
import json

from kit import run_calls


def signature(call):
    return f"{call['id']}:{call['name']}:{json.dumps(call['args'], sort_keys=True)}"


def run_agent(model, task, schemas, tools, max_steps=10, repeat_limit=3):
    messages = [{"role": "user", "content": task}]
    signatures = []
    steps = 0

    while steps < max_steps:
        reply = model.chat(messages, tools=schemas)
        steps = steps + 1
        messages.append(reply["message"])

        if reply["stop"] != "tools":
            return {"answer": reply["text"], "stopped": "done", "steps": steps}

        for call in reply["tool_calls"]:
            signatures.append(signature(call))
            if signatures.count(signatures[-1]) >= repeat_limit:
                return {"answer": "I kept repeating the same step, so I stopped.",
                        "stopped": "repeating", "steps": steps}

        messages.extend(run_calls(tools, reply["tool_calls"]))

    return {"answer": "I ran out of steps before finishing.",
            "stopped": "max_steps", "steps": steps}
