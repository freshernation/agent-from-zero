# Week 1 Milestone — Desk, version zero

> Everything you learned this week, in one program you wrote yourself.

A chatbot with no AI in it. It reads a line, decides what to say, and goes round again
until it is told to stop. You will meet this loop again in week 6.

---

## What it must do

Keep asking `You: ` and answering, until the person types `quit`.

| The person types | The bot prints |
|---|---|
| `hello` | `Bot: Hi! I am Desk.` |
| `help` | `Bot: I know: hello, help, count, quit.` |
| `count` | `Bot: You have sent 3 messages.` — including this one |
| nothing at all | `Bot: Say something.` — and this does **not** count as a message |
| anything else, e.g. `pizza` | `Bot: I don't know "pizza" yet.` |
| `quit` | `Bot: Bye! We exchanged 5 messages.` — including this one — then stop |

Capitals and spaces around a command do not matter: `  HELP ` is `help`.

### Worked example

```
You: hello
Bot: Hi! I am Desk.
You: pizza
Bot: I don't know "pizza" yet.
You:
Bot: Say something.
You: count
Bot: You have sent 3 messages.
You: quit
Bot: Bye! We exchanged 4 messages.
```

---

## Check it

```bash
pytest week-01/milestone -v
```

---

## Then make it good

Green tests mean it behaves correctly. They say nothing about whether the code is any
good, and on Friday you will be asked about the code, not the output.

Open `ai/editor.md` in a fresh chat, paste this spec and your code, and work through
what it finds. Before Friday:

- [ ] Every variable name says what it holds. No `x`, `n`, `t`.
- [ ] The text is tidied **once**, not in every `if`.
- [ ] You can point at the one line that decides whether the loop goes round again.
- [ ] You could explain **every single line** to someone who has never seen it.

---

## Friday

1. **Rehearsal.** Run `ai/defend.md` on your own code first.
2. **The real one.** Your instructor runs the same three phases, live, and will change
   the requirements while you watch.

You pass at 3 out of 5 in every phase. Not on average.
