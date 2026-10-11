# Day 4 — Debug an agent

> **By the end of today** you can find a bug in an agent loop — including the kind
> where the agent still works and only the bill is wrong.

No new ideas today. Four broken agents.

---

## What you need to know

### The fake model is your debugger

Every rule a real API enforces about the message list, the fake enforces too, and it
explains itself. When you see `InvalidRequest`, **read the whole message**. It names
the position in the list and says what was expected there.

### Print the list

When the order of messages is in doubt, look at it:

```python
for position, message in enumerate(messages):
    print(position, message["role"], message.get("tool_call_id", ""),
          [call["id"] for call in message.get("tool_calls", [])])
```

Six lines of output will show you what an hour of staring will not.

### Count the calls

`model.call_count` after a run is the single most useful number in agent debugging.
An agent that should take three steps and took ten is broken, even if its answer is
right. **A correct answer is not evidence of a correct agent.**

### The four families of loop bug

| Family | Symptom |
|---|---|
| **Order** — things appended in the wrong sequence | the API rejects the request |
| **Coverage** — some calls never answered | the API rejects the request, but only when there are two or more calls |
| **Termination** — the counter or the exit is wrong | it never stops, or stops one step early or late |
| **Silent** — a guard that can never fire | everything works; it just costs three times as much |

The last family is the one that reaches production.

---

## Exercises

```bash
pytest week-06/day-4 -v
```

`broken_1.py` to `broken_4.py` each hold a small `run_agent`. The comment at the top
says what is expected. Fix each with the smallest change you can — every one is a
single line — and fill in `NOTES.md`.

Do **not** paste your own agent over them. Finding the line is the exercise.

---

## Before you close the laptop

Commit, push, fill in the signal log.
