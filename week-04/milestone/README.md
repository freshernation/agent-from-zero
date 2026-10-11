# Week 4 Milestone — Desk can talk

> A chat assistant with a memory and a meter, that runs on any provider.

Week 1's bot answered from an `if` ladder. This one answers from a model. Look at how
little of the loop changes.

---

## `assistant.py`

### `new_session(system)`

Returns the state of one conversation:

```python
{"system": system, "history": [], "usage": {"input": 0, "output": 0}}
```

### `handle(model, session, line)` → the reply, as a string

| The line | Does | Returns |
|---|---|---|
| empty or only spaces | nothing | `Say something.` |
| `/turns` | nothing | `2 turns so far.` — the number of user messages in the history |
| `/cost` | nothing | `Tokens: 40 in, 12 out. Cost: $0.0004` — four decimals, using `PRICE_IN` and `PRICE_OUT` from the top of the file |
| `/reset` | empties the history; **keeps** the usage | `Conversation cleared.` |
| anything else | sends it to the model with the session's system prompt and the whole history; adds the reply's tokens to `session["usage"]` | the model's text |

Commands may be in any capitals. Two more rules for the last row:

- If the reply was cut off (`stop` is `"length"`), return the text followed by
  ` [cut off]`.
- If the model raises `ModelError`, return `The model is unavailable: <the error's
  message>`, and leave the history exactly as it was.

`handle` does no printing and no `input()`.

### `main()`

Connect with `connect()`. Make a session with a system prompt of your own — who is
Desk, and how should it talk? Loop on the prompt `You: `. Print each reply as
`Desk: <reply>`. On `quit`, print the `/cost` line and then `Bye.`

Call `main()` behind the `__name__` guard.

---

## Check it

```bash
pytest week-04/milestone -v
python3 week-04/milestone/assistant.py
```

Then set `AGENT_PROVIDER` to a real provider in `.env` and have an actual conversation.
Tell it your name, talk about something else for three turns, then ask what your name
is. Type `/reset` and ask again. Type `/cost` and look at the number.

---

## Then make it good

- [ ] The model is called in exactly one place.
- [ ] Your system prompt says who the user is and what a good answer looks like.
- [ ] You can point at the line that makes the model "remember".
- [ ] You know your real prices, and `PRICE_IN` / `PRICE_OUT` hold them.

---

## Friday

Rehearse with `ai/defend.md`, then the real defence.
