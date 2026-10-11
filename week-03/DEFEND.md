# Week 3 — Friday defence · Project 1

Thirty minutes. The student shares the four milestone files.

---

## Phase 1 — Explain (8 min)

1. *"Which file would change if notes were stored in a database instead? Which would not?"*
2. *"`handle` returns a string and never prints. What did that buy you this week?"*
3. *"Point at every `except` in the project and tell me which error it names and when
   that error actually happens."*
4. *"Why does `calculate` raise but `calculate_tool` return?"* — looking for: one is for
   programmers, the other for a caller that cannot read a traceback.
5. *"What runs when another file does `import app`?"*

## Phase 2 — Mutate (10 min)

- **A** — *"Add an `edit <title> | <new body>` command."* Name the files that change
  **and the ones that do not** before typing. Looking for: a new function in
  `notes.py` that returns a sentence, one branch in `handle`, nothing in `store.py`.
- **B** — *"Saving after every command is slow. Save only when something changed."*
  Discussion first: how does `main` know? Looking for a real answer (compare before and
  after, or have `handle` say so) and an honest account of its cost.

## Phase 3 — Break (7 min)

Seed one before they arrive.

| Seed | Break | Probes |
|---|---|---|
| Easy | `"**"` check removed from `calculate` | Do they remember why it was there? |
| Medium | `except json.JSONDecodeError` becomes `except ValueError` in `store.py` | Still works — `JSONDecodeError` is a kind of `ValueError`. Can they explain why the test still passes? |
| Hard | `save_notes` moved above `print(handle(...))` | Saves the state from *before* the command. Loses the last note on quit. |

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Explain** | Gives each file's single reason to change | Describes each file correctly | Cannot say why there are four |
| **Mutate** | Names what does not change | Finds the changes by running | Edits `store.py` for a notes feature |
| **Break** | Reproduces, isolates, one change | Finds it | Guesses |

Pass is 3 in every phase.

---

## Say this before they leave

> **`handle` reads a line and decides which function to call. That is the job you are
> about to give away. From week 5 the model reads the line, the model picks the
> function, and you keep everything else you built this week.**
