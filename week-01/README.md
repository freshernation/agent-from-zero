# Week 1 — Code is not magic

> **Destination**
> Write, save, and run a Python program that keeps talking to a person until they tell
> it to stop.

By Friday you will have written a small chatbot with no AI in it at all — a loop that
reads a line, decides what to say, and goes round again. Hold on to that shape. In
week 6 you will write it once more, with a model making the decision, and it will be
called an agent.

Weeks 1–3 are **AI-off for writing code**. The model tutors you (`ai/tutor.md`) and
never authors for you.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Run a file, store values, and print exactly what you meant |
| Tue | `day-2/` | Do arithmetic on what a person types, and choose between paths |
| Wed | `day-3/` | Repeat something until a condition says stop |
| Thu | `day-4/` | Read a traceback and fix code you did not write |
| Fri | `milestone/` | Ship the rule-based chatbot, then defend it |

Each day folder has its own `README.md`. Start there, every time.

---

## How a day goes

1. **Read** the day's README. All of it, before writing anything.
2. **Predict, then run.** Before you run any file, say out loud what you think it will
   print. Being wrong here is worth more than being right.
3. **Write** the exercises. In order — they build.
4. **Test** with `pytest week-01/day-N -v`. Green means correct behaviour, nothing more.
5. **Log** anything that stuck you in `logs/stuck-log.md`, and your numbers in
   `logs/signal-log.md`.
6. **Commit and push.** Every day.

---

## Milestone

A chatbot that answers four commands and counts the conversation. Spec in
`milestone/README.md`. It must pass its tests **and** survive Friday's defence, which
is a different and harder bar.

---

## Outside-view question

Once this week, open `ai/outside-view.md` and ask it this:

> *How does a restaurant waiter decide what to do next, and how is that like a program
> with a `while` loop?*

It is not on any test. It is how the idea stops being about Python.

---

## What this week is not about

Elegance. Speed. Anything in the "not yet" column of `FENCE.md`. You will write clumsy
code this week and that is correct. Clumsy code you understand completely beats elegant
code you copied, and it is not close.
