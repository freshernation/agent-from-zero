# Day 3 — When it goes wrong

> **By the end of today** your agent survives a tool that fails, a model that repeats
> itself, a result too big to send back, and a reply that never finishes.

Monday's agent works when everything goes right. Real agents spend most of their
steps somewhere else.

---

## Read first

- [ ] Anthropic — [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) — the sections on tool responses and errors · 20 min
- [ ] OpenAI — [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — "Guardrails" · 15 min

---

## What you need to know

### 1. A failed tool is information

`run_tool` already turns every failure into a sentence. So when the model asks for
`find_notes` with no arguments, it gets back *"Error: TypeError: find_notes() missing 1
required positional argument: 'word'"* — and on the next step it calls it properly.
You do nothing. The loop **is** the retry mechanism. Today you write the test that
proves it.

### 2. Repeating

Sometimes the model asks for exactly the same thing again. And again. The cap would
catch it at step ten; catching it at three costs a third as much.

To notice, give every call a **signature** — a string that is identical for identical
calls:

```python
json.dumps({"b": 2, "a": 1}, sort_keys=True)     # '{"a": 1, "b": 2}'
```

`sort_keys=True` matters. `{"a": 1, "b": 2}` and `{"b": 2, "a": 1}` are the same
arguments and must give the same signature. Leave it off and the check silently never
fires — that is tomorrow's nastiest bug.

Keep a list of every signature so far. If the newest one has now appeared `limit`
times, stop — **before** running it again.

### 3. Results that are too big

A tool that returns a 200,000-character file sends 200,000 characters to the model on
this step and on every step after it. Clip long results, and **say that you did**:

```
...first 2000 characters... [3000 more characters cut]
```

Telling the model it was cut is the difference between a model that knows it is
missing something and a model that confidently answers from half a document.

### 4. The other values of `stop`

| `stop` | Meaning | What the agent does |
|---|---|---|
| `"done"` | finished | return the answer |
| `"tools"` | wants tools | run them, go round |
| `"length"` | cut off mid-reply | stop; return the text with ` [cut off]` on the end |
| `"refused"` | declined | stop; return `The model declined this request.` |

Monday's `if reply["stop"] != "tools": return` treats a cut-off half-sentence as a
finished answer. Check each value by name.

### 5. The model itself failing

`model.chat` can raise `ModelError`. An agent that crashes on step seven throws away
six steps of work. Catch it, stop cleanly, and return what you have.

### How a run can end, now

| `stopped` | `answer` |
|---|---|
| `done` | the model's text |
| `max_steps` | `I ran out of steps before finishing.` |
| `repeating` | `I kept repeating the same step, so I stopped.` |
| `length` | the model's text + ` [cut off]` |
| `refused` | `The model declined this request.` |
| `error` | `The model is unavailable: <message>` |

Every ending except `done` adds one last trace event:
`{"step": <steps>, "kind": "stop", "reason": <stopped>}`.

---

## Exercises

```bash
pytest week-06/day-3 -v
```

### 1. `guards.py`

| Function | Returns |
|---|---|
| `signature(call)` | a string that is the same for two calls with the same name and the same arguments, in any key order |
| `is_repeating(signatures, limit=3)` | `True` if the **last** signature in the list appears at least `limit` times in it |
| `clip(text, limit=2000)` | the text unchanged if it fits; otherwise its first `limit` characters followed by `... [3000 more characters cut]` |

### 2. `agent.py`

Copy yesterday's `agent.py` here and grow it:

```python
run_agent(model, task, schemas, tools, system=None,
          max_steps=10, repeat_limit=3, result_limit=2000)
```

All six endings from the table. Tool results are clipped to `result_limit` — in the
messages **and** in the trace. A `ModelError` does not count as a step.

---

## Predict-then-run

Your agent has `max_steps=10` and `repeat_limit=3`. The model asks for
`list_titles` over and over. How many times is the **model** called? How many times
does the **tool** run? They are different numbers.

---

## Before you close the laptop

Commit, push, fill in the signal log.
