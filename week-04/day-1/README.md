# Day 1 — The first call

> **By the end of today** you can send a question to a model, steer how it answers, and
> read every part of what comes back.

---

## Read first

Read the one for the provider you will use. Skim the other on Thursday.

- [ ] Claude — [Working with the Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages) · 15 min
- [ ] OpenAI — [Text generation](https://developers.openai.com/api/docs/guides/text) · 15 min

Both pages use the provider's own package. You use `llm` instead; the ideas are
identical and Thursday shows you the mapping.

---

## What you need to know

### The request is a list of messages

```python
from llm import connect

model = connect()
reply = model.chat([{"role": "user", "content": "What is the capital of Peru?"}])
print(reply["text"])        # Lima.
```

Even a single question is a **list** with one message in it. Tomorrow the list grows.

### The system prompt

The messages are the conversation. The **system prompt** is the standing instruction
that sits above it: who the model is being, how it should answer, what it must not do.

```python
reply = model.chat(
    [{"role": "user", "content": "What is the capital of Peru?"}],
    system="Answer in one word.",
)
```

It is **not** a message and it does not go in the list. It is a separate argument.

A good system prompt says who the reader is and what a good answer looks like. *"You
are helping a beginner programmer. Use plain words and one short example."* beats *"Be
helpful."* every time.

### Reading the reply

```python
reply["text"]             # "Lima."
reply["stop"]             # "done"
reply["usage"]            # {"input": 14, "output": 3}
```

`stop` is the field beginners ignore and professionals check first. `"done"` means the
model finished. `"length"` means it ran out of room mid-sentence. `"refused"` means it
declined. Next week a fourth value arrives and it changes everything.

### Tokens

Models do not count words or characters. They count **tokens** — pieces of words,
roughly four characters each in English. `usage` tells you how many went in and how
many came out, and that is what you are billed for.

### Why your functions take `model`

```python
def ask(model, question):       # yes
    ...

def ask(question):              # no
    model = connect()           # now this cannot be tested without a key
    ...
```

---

## Exercises

```bash
pytest week-04/day-1 -v
python3 week-04/try_it.py
```

All in `ask.py`.

| Function | Returns |
|---|---|
| `ask(model, question)` | the text of the model's answer |
| `ask_as(model, system, question)` | the same, with that system prompt |
| `describe(reply)` | `"done: 14 tokens in, 3 out"` |
| `short_answer(model, question)` | the answer, using a system prompt **you** write that makes the model reply in ten words or fewer |

For `short_answer` the tests can only check that you sent a real system prompt. Whether
it *works* you find out by running it against a real model — do that.

---

## Predict-then-run

With a real provider, run `try_it.py` three times. Is the answer the same each time?
Now change the system prompt to *"Answer as a pirate."* What changed, and what did not?

---

## Before you close the laptop

Commit, push, fill in the signal log. **Check that `.env` is not in your commit.**
