# Day 2 — It has no memory

> **By the end of today** you can hold a conversation with a model, and say exactly
> where the "memory" lives. (In your list. Nowhere else.)

---

## Read first

- [ ] Claude — [Multiple conversational turns](https://platform.claude.com/docs/en/build-with-claude/working-with-messages#multiple-conversational-turns) · 5 min
- [ ] OpenAI — [Conversation state](https://developers.openai.com/api/docs/guides/conversation-state) — the "manually manage" section · 10 min

---

## What you need to know

### Every call is the first one

```python
model.chat([{"role": "user", "content": "My name is Sam."}])
model.chat([{"role": "user", "content": "What is my name?"}])    # it does not know
```

The model keeps nothing between calls. There is no session, no thread, no memory on
the other end.

### A conversation is a list you keep resending

```python
history = []

history.append({"role": "user", "content": "My name is Sam."})
reply = model.chat(history)
history.append(reply["message"])          # <- what the model said, back into the list

history.append({"role": "user", "content": "What is my name?"})
reply = model.chat(history)               # all three earlier lines go again
history.append(reply["message"])
```

On the second call the model sees the whole exchange and answers "Sam". It has not
remembered anything. You told it again.

### Append `reply["message"]`, not your own copy

`reply["message"]` is the assistant's turn exactly as the provider needs to see it
again. Do not rebuild it from `reply["text"]`. From next week it carries tool calls,
and some providers attach private reasoning that must come back untouched.

### The rules of the list

A real API rejects a conversation that breaks these, and so does the fake:

- It starts with a `user` message.
- The same speaker never goes twice in a row.
- When you call the model, the last message is **not** the model's own.

### Cleaning up after a failure

If the model call fails, your list now ends with a user message that never got an
answer. The next `send` would add a second user message in a row. So undo first, then
pass the error on:

```python
history.append(question)
try:
    reply = model.chat(history)
except ModelError:
    history.pop()        # remove the message that never got an answer
    raise                # a bare `raise` re-raises the same error
```

### What this costs

Turn 1 sends 1 message. Turn 2 sends 3. Turn 10 sends 19. The whole history is input
tokens **every time**, so a long chat gets more expensive with every turn. Week 7 is
partly about that.

---

## Exercises

```bash
pytest week-04/day-2 -v
```

All in `chat.py`.

| Function | Does |
|---|---|
| `send(model, history, text, system=None)` | appends the user's message, calls the model with the **whole** history, appends the model's turn, returns its text. If the call raises `ModelError`, `history` is left exactly as it was and the error is passed on |
| `turns(history)` | how many `user` messages there are |
| `reset(history)` | empties **that** list (`history.clear()`) and returns nothing |

---

## Predict-then-run

In a scratch file, with a real provider: send *"Pick a number between 1 and 100 and
remember it."*, then call `reset(history)`, then send *"What was your number?"*. What
does it say? What does that prove about where the memory was?

---

## Before you close the laptop

Commit, push, fill in the signal log.
