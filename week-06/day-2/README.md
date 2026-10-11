# Day 2 — Watch it think

> **By the end of today** your agent leaves a record of every step it took and what
> the run cost, and you can read that record at a glance.

Yesterday's agent returned an answer and a number. If the answer was wrong you had no
way to know why. An agent you cannot observe is an agent you cannot debug — and
Thursday is going to need this.

---

## Read first

- [ ] Anthropic — [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — re-read "Agents" and the three principles at the end · 10 min
- [ ] OpenAI — [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — "Agent design foundations" · 15 min

---

## What you need to know

### A trace is a list of events

Not `print` statements — data. A list of small dictionaries, appended to as the run
goes, returned with the result. Data can be printed, saved, counted and tested;
printed text can only be read.

```python
trace = []
...
trace.append({"step": steps, "kind": "call", "name": call["name"], "args": call["args"]})
```

### The five kinds of event

| `kind` | When | Other keys |
|---|---|---|
| `say` | the model said something **and** asked for tools in the same turn | `text` |
| `call` | once per tool the model asked for | `name`, `args` |
| `result` | once per tool result | `name`, `content` |
| `answer` | the model finished | `text` |
| `stop` | **you** ended the run | `reason` |

Every event carries `step` — which trip to the model it belongs to.

Within one step the order is: `say` (if there is any text), then every `call`, then
every `result`.

### Pairing calls with results

`run_calls` gives back one message per call, in the same order. `zip` walks two lists
side by side:

```python
for call, message in zip(reply["tool_calls"], results):
    trace.append({"step": steps, "kind": "result",
                  "name": call["name"], "content": message["content"]})
```

### Cost

Every `reply` has a `usage`. Add them up as you go — that total is what the run cost,
and because the whole history is resent every step, it grows faster than you expect.
A ten-step run does not cost ten times a one-step run. It costs more like fifty.

### What a trace looks like, printed

```
[1] call add_note({"title": "rent", "body": "1450 a month"})
[1] result add_note: Saved 'rent'.
[2] say: Now the yearly figure.
[2] call calculate({"expression": "1450 * 12"})
[2] result calculate: 17400
[3] answer: Saved. That is 17400 a year.
```

When an agent does something stupid, this is where you will see it. Nine times in ten
the model was handed a misleading tool result and reasoned perfectly from it.

---

## Exercises

```bash
pytest week-06/day-2 -v
```

### 1. `agent.py`

Copy yesterday's `agent.py` here. Add two keys to the result, on **both** exits:

| Key | Holds |
|---|---|
| `"usage"` | `{"input": ..., "output": ...}` — summed over every model call |
| `"trace"` | the list of events, as described above. When the cap ends the run, the last event is `{"step": <steps>, "kind": "stop", "reason": "max_steps"}` |

### 2. `show.py`

| Function | Returns |
|---|---|
| `format_event(event)` | one line, exactly as in the printed example above. Arguments are shown with `json.dumps(args)`. A `stop` event is `[4] stop: max_steps` |
| `format_trace(trace)` | every event's line, joined with newlines |
| `summary(result)` | `done in 3 steps (300 tokens in, 60 out)` |

Then run `python3 week-06/day-2/try_trace.py` against a real provider and read what
your agent actually did.

---

## Predict-then-run

A three-step run where every reply uses 100 input tokens *more* than the one before,
starting at 100. What is the total input? Now ten steps. This is why week 7 has a day
on memory.

---

## Before you close the laptop

Commit, push, fill in the signal log.
