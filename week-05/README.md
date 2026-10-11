# Week 5 — Tools

> **Destination**
> Describe a function to a model, receive its request to call one, run it, and hand
> back the result — and know that the model never ran anything.

Until now the model could only talk. This week it gets hands. And the single most
important sentence in the course is this one:

> **The model never executes anything. It asks. You run it.**

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Describe a function so that a model can decide when to use it |
| Tue | `day-2/` | Run the function a model asked for — safely, whatever it asked |
| Wed | `day-3/` | Complete one full round trip: ask, run, answer |
| Thu | `day-4/` | Open the box again: tool calls in Claude's dialect and OpenAI's |
| Fri | `milestone/` | Ship Desk with hands — a chat assistant that can use your notes |

---

## What a "tool" actually is

Three ordinary things, and no magic anywhere.

1. **A schema** — a dictionary describing a function: its name, what it is for, and
   its arguments. You send it along with the conversation.
2. **A request** — the model replies with `stop` set to `"tools"` and a list saying
   *"please call `add_note` with `{"title": "milk"}`"*. It has not run anything. It
   cannot. It wrote some JSON.
3. **A dispatch table** — your dictionary of `{"add_note": add_note}`. **You** look up
   the name, **you** call the function, and **you** send the result back as one more
   message in the list.

Every agent framework in existence wraps those three things. By Wednesday you will
have written all of them.

---

## `toolbox.py` is given

It holds five finished functions — `add_note`, `list_titles`, `find_notes`,
`delete_note`, `calculate` — which are your week 2 and week 3 code, saving to a JSON
file. Read it once. Notice that nothing in it mentions a model. A copy sits in each
folder that needs it.

---

## The shapes, for reference

A tool **schema**:

```python
{"name": "add_note",
 "description": "Save a new note with a title and an optional body. Use when ...",
 "parameters": {"type": "object",
                "properties": {"title": {"type": "string", "description": "..."}},
                "required": ["title"]}}
```

A tool **call**, inside `reply["tool_calls"]`:

```python
{"id": "call_1", "name": "add_note", "args": {"title": "milk"}}
```

A tool **result**, which you append to the list:

```python
{"role": "tool", "tool_call_id": "call_1", "content": "Saved 'milk'."}
```

---

## Outside-view question

> *How does a head chef describe a dish to a new cook who cannot taste it, and what
> does that tell you about writing a tool description?*
