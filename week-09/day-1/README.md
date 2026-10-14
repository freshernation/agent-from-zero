# Day 1 — Decide

> **By the end of today** `project/SPEC.md` is filled in, and you have said *no* to
> at least five things.

No code today. The most expensive mistakes in an agent project are made before the
first line is written: too many tools, no idea what "working" means, nothing ruled out.

---

## Read first

- [ ] Anthropic — [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — "When (and when not) to use agents" · 10 min
- [ ] Anthropic — [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) — "Choosing the right tools" · 15 min

---

## The five decisions

This course was planned by answering five questions. Answer the same five for your
project.

| Decision | The question |
|---|---|
| **Destination** | What can a user do with this that they could not do before? One sentence |
| **Baseline** | What already exists — the file, its shape, a few real rows of data |
| **Sequence** | Which tool do you build first, and which request works first |
| **Cut list** | What will it **not** do this week |
| **Milestone** | Which eval cases prove it works |

`project/SPEC.md` has a section for each.

---

## Designing the tools

Write the table before the code. For each tool: its name, its arguments, the sentence
it returns when it works, the sentence it returns when it fails, and whether it is
dangerous.

**Fewer, clearer tools beat more.** If two tools would have descriptions that begin
the same way, the model will not be able to choose between them either. Merge them.

**Design for the model, not for the database.** `get_record(id)` forces the model to
know an id. `find_book(title_or_author)` lets it work the way the user speaks.

**Every failure sentence should say what to do next.** *"No book called 'Dune'. Call
list_books to see the titles."* is a tool that helps the loop recover.

---

## Use the planner

Open `ai/planner.md` in a fresh chat. It will interview you, one question at a time,
through the five decisions. Let it push back on your cut list — it will usually tell
you it is too short.

---

## Check it

```bash
pytest week-09/project -k Spec -v
```

---

## Before you close the laptop

Commit, push, fill in the signal log. Send your instructor the spec **tonight** — a
project that is too big is much cheaper to shrink on Monday than on Thursday.
