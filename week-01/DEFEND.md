# Week 1 — Friday defence

Twenty minutes per student. The student shares their screen with `milestone/bot.py`.

---

## Phase 1 — Explain (5 min)

1. *"Point at the line that decides whether the loop goes round again."*
2. *"Why is `.strip().lower()` where it is? What breaks if you move it into the first `if`?"*
3. *"`count` says 3 and you have typed three things. Which line made that 3 and when did it run?"*
4. *"What does `input()` give you if I just press Enter?"*
5. *"Why does the empty line not add to the count? Show me the lines that make that true."*

## Phase 2 — Mutate (8 min)

Words first, keyboard second.

- **A** — *"Add a `name` command: the bot asks `Bot: What is your name?`, reads a line,
  and from then on `hello` answers `Bot: Hi, Sam! I am Desk.`"* Looking for: a new
  variable that outlives one trip round the loop.
- **B** — *"After 10 messages the bot says `Bot: That is enough for today.` and stops
  by itself."* Looking for: a second exit. Ask which exit fires first if message 10 is
  `quit`.

## Phase 3 — Break (5 min)

*"Give me an input that makes it misbehave."* Then seed one: change `sent = sent + 1`
to sit above the empty check and ask what the user would notice.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Explain** | Names the `break` and the condition unprompted | Describes the flow correctly | Reads the code aloud |
| **Mutate** | Names the lines before typing, including the second exit | Gets there by running it | Cannot place the new variable |
| **Break** | Predicts the miscounting | Finds it by running | Believes nothing breaks it |

Pass is 3 in every phase.

---

## Say this before they leave

> **You wrote a loop that reads something, decides, responds, and stops for one of two
> reasons. In five weeks you will replace the `if` ladder with a model and nothing else
> about the shape will change.**
