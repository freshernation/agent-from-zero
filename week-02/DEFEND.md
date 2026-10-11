# Week 2 — Friday defence

Twenty-five minutes. The student shares `milestone/notes.py`.

---

## Phase 1 — Explain (6 min)

1. *"`add_note` changes `notes` and also returns a sentence. Who is each of those for?"*
2. *"Where is the line that decides two titles are 'the same'? How many places is it written?"*
3. *"What does `find_notes` return when nothing matches — and why not an empty string?"*
4. *"Show me a function here that would return `None` if I deleted one line. Which line?"*
5. *"Why is `notes` an argument to every function instead of a variable at the top of the file?"*

## Phase 2 — Mutate (10 min)

- **A** — *"Add `rename_note(notes, old, new)`."* Name every sentence it can return
  before typing. Looking for: not found, new title already taken, new title empty.
- **B** — *"Notes now have a third key, `done`, and `list_titles` shows `[x]` or `[ ]`
  in front of each."* Looking for: where the key is first created, and what happens to
  notes that were made before the change (`.get`).

## Phase 3 — Break (5 min)

Seed before they arrive: in their `delete_note`, compare titles without `.lower()` on
one side. Ask them to delete `Milk`. Nothing crashes; the sentence says it was not
found. *"How would a user describe this bug to you?"*

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Explain** | "The list is for the program, the sentence is for whoever asked" | Describes each correctly when asked | Cannot separate changing from returning |
| **Mutate** | Lists all the return sentences first | Finds them as tests would | Writes the happy path only |
| **Break** | Goes straight to the comparison | Prints, then finds it | Edits at random |

Pass is 3 in every phase.

---

## Say this before they leave

> **Every function you wrote returns a sentence. In week 5 a model reads those
> sentences and decides what to do next. "No note called 'cheese'." is not an error
> message — it is how your agent will find out it guessed wrong.**
