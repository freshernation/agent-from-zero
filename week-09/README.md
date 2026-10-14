# Week 9 — Your agent

> **Destination**
> Design, build, measure and defend an agent for a problem **you** chose — and leave
> with a repository you can put in front of an employer.

For eight weeks the problem was notes, because notes are boring and the loop was the
lesson. The loop is yours now. This week the problem is whatever you pick.

There is no new material. There is a blank folder, a contract, and a Friday.

---

## The week

| Day | Folder | What you produce |
|---|---|---|
| Mon | `day-1/` | A one-page spec: what it does, what it must never do, and how you will know |
| Tue | `day-2/` | The tools, working and tested, with **no model anywhere near them** |
| Wed | `day-3/` | The agent wired up, and a first eval score against a real model |
| Thu | `day-4/` | Three attacks on your own agent, the fixes, and the write-up |
| Fri | `project/` | **Project 3** — demo and defence |

All of the work goes in `project/`. The day folders hold only that day's instructions.

---

## The contract

`project/test_contract.py` checks the shape of what you build — not what it is about.
Whatever your agent does, it must have:

- at least **four tools**, one of which **changes** something;
- every tool returning a sentence, even when handed nonsense;
- its data in **one JSON file** whose location comes from `DATA_FILE`;
- a decision, in code, about which tools are **dangerous**;
- at least **eight eval cases**, with a real report;
- a spec, and a README a stranger could follow.

---

## Choosing a problem

A good capstone agent:

- acts on **something you can inspect** — a JSON file of books, workouts, expenses,
  flashcards, plants, job applications, recipes;
- needs **more than one step** for its interesting requests;
- has at least one action you would **not** want done by accident.

Leave for after the course: sending email or messages, running shell commands,
browsing the web, touching anyone's real accounts, spending money. Not because they
are hard — because a mistake in them is not confined to your own laptop, and you have
had exactly one week of practice at preventing mistakes.

---

## Outside-view question

> *How does an architect decide what to leave out of a small house, and what should
> you leave out of a one-week agent?*

---

## What Friday is

A ten-minute demo against a real model, then a defence. Not of the code — of the
**decisions**. Why these tools. Why that one is gated. What your evals do not cover.
What you would not let it do.
