# Day 1 — Write the loop

> **By the end of today** you have written an agent: a loop that keeps asking the model
> until it is finished, or until you stop it.

---

## Read first

- [ ] Anthropic — [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — read all of it; it is the best single essay on the subject · 25 min
- [ ] Claude — [How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works) — the agentic loop section · 5 min

---

## What you need to know

### Last week, with the limit removed

```python
def run_agent(model, task, schemas, tools, system=None, max_steps=10):
    messages = [{"role": "user", "content": task}]
    steps = 0

    while steps < max_steps:
        reply = model.chat(messages, system=system, tools=schemas)
        steps = steps + 1
        messages.append(reply["message"])

        if reply["stop"] != "tools":
            return ...                       # it finished

        messages.extend(run_calls(tools, reply["tool_calls"]))

    return ...                               # you stopped it
```

Read it line by line. There is nothing in it you have not written before. The only
new thing is that step 4 of last Wednesday — *ask again* — is now the top of a loop.

### What makes it an agent

**The model decides how many times round it goes.** You did not write *"first list the
notes, then find the dentist one, then delete it"*. You wrote a loop, and the model
chose three steps. Give it a harder task and it will choose seven. That is the whole
idea, and it is also the whole risk.

### `steps` counts model calls

Not tools. One step is one trip to the model. A step may run three tools or none.

### The cap is not optional

`while True` around a model call is how people receive surprising invoices. A model
can ask for the same tool forever. The cap is the exit that works when everything else
has gone wrong.

### What to return

A bare string is not enough — the caller needs to know *how* it ended.

```python
{"answer": "17 times 23 is 391.",
 "stopped": "done",            # or "max_steps"
 "steps": 2,
 "messages": messages}
```

When the cap is hit there is no answer from the model, so the agent supplies one:
`I ran out of steps before finishing.`

---

## Exercises

```bash
pytest week-06/day-1 -v
```

Write `agent.py`:

| Function | Returns |
|---|---|
| `run_agent(model, task, schemas, tools, system=None, max_steps=10)` | the result dictionary above |

Import `run_calls` from `kit`. The `stopped` value is `"done"` when the model answered
and `"max_steps"` when the cap ended the run.

Then watch it work. With a real provider in `.env`:

```bash
python3 week-06/day-1/try_agent.py
```

It is given. It hands your agent a task that needs three steps.

---

## Predict-then-run

`try_agent.py` asks: *"Save a note that the rent is 1450 a month, then tell me what
that is per year."* How many **steps** will that take? How many **tools**? Write both
numbers down before you run it.

---

## Before you close the laptop

Commit, push, fill in the signal log.
