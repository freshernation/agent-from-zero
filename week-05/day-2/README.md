# Day 2 — Run what it asked for

> **By the end of today** you can take a model's request to call a function and run it
> — safely, whatever the model asked for.

Still no model today. You are writing the part of an agent that sits between *"the
model wants `add_note`"* and *"here is what happened"*.

---

## Read first

- [ ] Claude — [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) · 10 min
- [ ] [Unpacking argument lists](https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists) — the `**` half · 5 min

---

## What you need to know

### What the model sends

```python
reply["tool_calls"]
# [{"id": "call_1", "name": "add_note", "args": {"title": "milk", "body": "two litres"}}]
```

A name, a dictionary of arguments, and an id. That is all a tool call is.

### A dispatch table

Functions are values. You can put them in a dictionary:

```python
from toolbox import add_note, calculate

TOOLS = {
    "add_note": add_note,          # no brackets - the function itself, not a call
    "calculate": calculate,
}

function = TOOLS["calculate"]
function(expression="2 + 2")       # "4"
```

### `**` unpacks a dictionary into arguments

```python
args = {"title": "milk", "body": "two litres"}

add_note(**args)        # exactly the same as add_note(title="milk", body="two litres")
```

So running any tool the model asks for is one line: `TOOLS[name](**args)`.

### Everything that line can do wrong

| The model does this | Python does this |
|---|---|
| invents a tool name | `KeyError` |
| leaves out a required argument | `TypeError` |
| invents an extra argument | `TypeError` |
| asks for something the tool cannot do | whatever the tool raises |

Models do all four, and not rarely.

### The boundary rule

All term you have been told to name the error you catch. Here is the one exception.
At the exact spot where you run code on behalf of something you do not control, you
catch **everything**, and you turn it into a sentence:

```python
try:
    result = TOOLS[name](**args)
except Exception as error:
    return f"Error: {type(error).__name__}: {error}"
```

`type(error).__name__` is the error's name as text — `"TypeError"`, `"ValueError"`.

This is not hiding the error. It is **delivering** it — to the model, which can read
*"missing 1 required argument: 'word'"* and try again with the argument. A crash
teaches the model nothing and ends the conversation.

### The result is always a string

The message you send back carries text. `391` becomes `"391"`.

### One call in, one message out

```python
{"role": "tool", "tool_call_id": "call_1", "content": "Saved 'milk'."}
```

The `tool_call_id` must be the id of the call you are answering. With two calls in
flight it is the only thing connecting an answer to its question.

---

## Exercises

```bash
pytest week-05/day-2 -v
```

All in `dispatch.py`. `toolbox.py` is in this folder.

| Name | What it is |
|---|---|
| `TOOLS` | the dispatch table — all five names from `toolbox.py`, each mapped to its function |
| `run_tool(name, args)` | runs it and returns the result **as a string**. Never raises. A name that is not in `TOOLS` gives `Error: unknown tool 'xyz'`. Anything that goes wrong while running gives `Error: <ErrorName>: <message>` |
| `run_calls(tool_calls)` | a list of `tool` messages, one per call, in the same order |

---

## Predict-then-run

```python
def greet(name):
    return f"Hello, {name}"

greet(**{"name": "Sam", "mood": "happy"})
```

Read the error out loud. Now imagine you are a model and that sentence is all you get
back. Could you fix your call?

---

## Before you close the laptop

Commit, push, fill in the signal log.
