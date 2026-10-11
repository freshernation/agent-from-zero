# Week 5 Milestone — Desk with hands

> A chat assistant that can read and change your notes — one step at a time.

Week 4's assistant, plus week 5's tools. It keeps a conversation going across turns,
and inside each turn it may use tools **once**.

---

## The files

| File | Where it comes from |
|---|---|
| `toolbox.py` | given |
| `schemas.py` | **copy from day 1** |
| `dispatch.py` | **copy from day 2** |
| `desk.py` | new |

## `desk.py`

### `SYSTEM`

A system prompt, as a string, that you write. It should tell the model who it is, that
it has tools for the user's notes, and at least one rule about care — for example, to
check the list before deleting, or never to guess a title. At least 25 words.

### `respond(model, history, text)` → the reply, as a string

One turn of conversation, with `history` carried between turns exactly as in week 4.

1. Append the user's message.
2. Call the model with the whole history, `SYSTEM`, and the tools.
3. If it asked for tools: append its turn, run the calls, append the results, and call
   the model once more.
4. Append the model's final turn and return its text.

Three rules:

- If the model asks for tools a **second** time in one turn, do **not** append that
  unfinished turn. Return `I could not finish that in one step.` The history must stay
  legal — the next `respond` has to work.
- If the model raises `ModelError` on the **first** call of a turn, remove the user's
  message again and return `The model is unavailable: <message>`.
- `respond` does no printing and no `input()`.

### `main()`

`connect()`, an empty history, loop on `You: `, print `Desk: <reply>`, stop on `quit`
with `Bye.` Behind the `__name__` guard.

---

## Check it

```bash
pytest week-05/milestone -v
python3 week-05/milestone/desk.py          # with a real provider in .env
```

Have a real conversation. *"Remember I need to renew my passport by June."* Then
*"What do I have on?"* Then *"Delete the passport one."* Then open `notes.json` and see
what a model did to a file on your computer because you let it.

Now try: *"Delete all my notes."* Watch what happens, and write down why.

---

## Then make it good

- [ ] The model is called in one place, not copied twice.
- [ ] Your system prompt contains a rule you can show changing the model's behaviour.
- [ ] You can draw the message list after a tool turn, from memory, with roles.

---

## Friday

Rehearse with `ai/defend.md`, then the real defence.
