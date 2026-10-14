# Day 1 — Describe it

> **By the end of today** you can describe a function to a model well enough that it
> knows when to use it, and when not to.

No model calls a tool today. Today is the part people skip, and then spend a week
debugging: the description.

---

## Read first

- [ ] Claude — [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) · 15 min
- [ ] Claude — [How to implement tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) — "Best practices for tool definitions" · 10 min
- [ ] OpenAI — [Function calling](https://developers.openai.com/api/docs/guides/function-calling) — "Defining functions" · 10 min

---

## What you need to know

### A schema is a dictionary

```python
CALCULATE = {
    "name": "calculate",
    "description": (
        "Evaluate a basic arithmetic expression such as '17 * 23'. "
        "Use for any arithmetic rather than working it out yourself. "
        "Supports only + - * / and parentheses."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The arithmetic to evaluate, e.g. '(2 + 3) * 4'.",
            },
        },
        "required": ["expression"],
    },
}
```

The `parameters` part is a standard called **JSON Schema**. `properties` lists each
argument and its type; `required` lists the ones that must be present. A tool that
takes no arguments has `"properties": {}` and `"required": []`.

### The description is the prompt

It is the **only** thing the model knows about your function. Not the code, not what
you meant. A vague description produces a tool that is called at the wrong moments
with the wrong arguments, and the fix is always in the description, never in the code.

| Weak | Strong |
|---|---|
| "Adds a note" | "Save a new note with a short title and an optional body. Use when the user asks you to remember, save, or write something down." |
| "Deletes a note" | "Permanently delete the note with this exact title. This cannot be undone. Call list_titles first if you are not sure of the title." |

Say **what it does**, **when to use it**, and — often most usefully — **when not to**,
and what to do first.

### Argument descriptions matter too

`"title": {"type": "string"}` tells the model the type. `"description": "A short
title, a few words, e.g. 'call the dentist'"` tells it what to put there.

### Sending them

```python
reply = model.chat(messages, tools=[CALCULATE, ADD_NOTE])
```

You pass the **schemas** — the dictionaries. Not the functions. The model never sees
your code.

---

## Exercises

```bash
pytest week-05/day-1 -v
```

All in `schemas.py`.

| Name | What it is |
|---|---|
| `text_param(description)` | returns `{"type": "string", "description": description}` |
| `make_schema(name, description, properties, required)` | returns a schema dictionary in the shape above |
| `SCHEMAS` | a list of five schemas, one for each function in `toolbox.py`, in this order: `add_note`, `list_titles`, `find_notes`, `delete_note`, `calculate` |

Open `week-05/toolbox.py` and read each function's arguments before you describe it.
The names in your schema must match the function's parameter names **exactly** —
tomorrow they are passed straight through.

The tests check the structure, and three things about your words:

- every tool description is at least ten words,
- every argument has a description,
- `delete_note` warns that it cannot be undone.

They cannot check whether your descriptions are *good*. That you find out on Wednesday.

---

## Predict-then-run

You give a model the `calculate` tool and ask *"What is the capital of France?"*
Does it call the tool? Should it? Which words in your description decide?

---

## Before you close the laptop

Commit, push, fill in the signal log.
