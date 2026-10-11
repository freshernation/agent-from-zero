# Day 3 — The round trip

> **By the end of today** you have completed one full exchange: the model asks for a
> tool, you run it, and the model answers using the result.

Monday's schemas and Tuesday's dispatch meet a model. This is the first time anything
in this course *acts*.

---

## Read first

- [ ] Claude — [How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works) · 10 min
- [ ] OpenAI — [Function calling](https://platform.openai.com/docs/guides/function-calling) — "The tool calling flow" · 10 min

---

## What you need to know

### Four steps

```python
messages = [{"role": "user", "content": "What is 17 times 23?"}]

# 1. Ask, offering the tools.
reply = model.chat(messages, tools=SCHEMAS)

# 2. Did it answer, or did it ask for something?
if reply["stop"] != "tools":
    return reply["text"]                       # it just answered. Done.

# 3. It asked. Record what it said, run what it asked for, record the results.
messages.append(reply["message"])              # the model's turn - tool calls included
messages.extend(run_calls(reply["tool_calls"]))    # one "tool" message per call

# 4. Ask again. Now the list contains the question, the request, and the result.
reply = model.chat(messages, tools=SCHEMAS)
return reply["text"]
```

`list.extend(other)` appends every item of another list.

### What the list looks like at step 4

```python
[
  {"role": "user",      "content": "What is 17 times 23?"},
  {"role": "assistant", "content": "", "tool_calls": [{"id": "call_1", "name": "calculate", ...}]},
  {"role": "tool",      "tool_call_id": "call_1", "content": "391"},
]
```

The model has no memory, remember. It only knows it asked for `calculate` because you
sent its own request back to it. And it only knows the answer because you put it in
the list.

### The two mistakes everybody makes once

**Forgetting to append `reply["message"]`.** Then the model is handed an answer to a
question it has no record of asking. A real API rejects this, and so does the fake —
read its error message when you meet it.

**Leaving a call unanswered.** If the model asked for three tools, three results go
back, even if two of them are error messages. A call with no result is also rejected.

### Offer the tools on the second call too

The model needs the schemas to make sense of the tool calls in the history.

### A model that only wants to talk

Ask *"hello"* and `stop` is `"done"` with no tool calls. Offering tools does not
oblige the model to use them. Your code must handle both.

### And if it asks again?

After seeing a result the model may ask for **another** tool. Today you stop there and
say so. Handling it properly is a loop, and the loop is next week.

---

## Exercises

```bash
pytest week-05/day-3 -v
```

First copy your `schemas.py` from day 1 and your `dispatch.py` from day 2 into this
folder. Then write `round_trip.py`:

| Function | Does |
|---|---|
| `answer(model, schemas, question, system=None)` | the four steps above, returning the model's final text. If the model asks for tools a **second** time, return `I could not finish that in one step.` |

Then try it for real. With a real provider in `.env`:

```bash
python3 week-05/day-3/try_tools.py
```

That script is given. It asks three questions; watch which ones make the model reach
for a tool. If it picks the wrong tool, or none, **the fix is in your descriptions**.

---

## Predict-then-run

Before running `try_tools.py`: which of its three questions will use a tool? Which
tool? Write it down. Then check.

---

## Before you close the laptop

Commit, push, fill in the signal log.
