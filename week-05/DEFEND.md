# Week 5 — Friday defence

Thirty-five minutes. The student shares `milestone/desk.py` and runs it against a real
provider.

---

## Phase 0 — The sentence (1 min)

> *"Does the model ever run your code?"*

**No.** Then: *"So what does it do?"* — it writes JSON naming a function and its
arguments. If they cannot separate the request from the execution, nothing else this
week has landed.

## Phase 1 — Explain (8 min)

1. *"Show me the message list after a turn that used a tool. Roles, in order."* On
   paper, before they look at the screen.
2. *"Why does the model's own turn go back into the list before the results do?"*
3. *"What is the id for, and when would getting it wrong become visible?"* — only with
   two calls in flight.
4. *"`run_tool` catches `Exception`. All term I told you not to. Defend it."*
5. *"Every tool returns a string, even when it fails. Argue for that."*

## Phase 2 — Mutate (12 min)

- **A** — *"Add a `count_notes` tool."* Name the **three** places before typing: the
  function, the schema, the dispatch table. Then ask what its description should say
  to stop the model using `list_titles` and counting.
- **B** — live, with a real model: *"Your model deleted the wrong note. Change one
  thing — not code — to make that less likely."* Looking for: the description or the
  system prompt, then re-run to show it.

## Phase 3 — Debug (8 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | a schema argument renamed `text` while the function takes `word` | The tool returns a `TypeError` sentence. Do they read it as the model would? |
| Medium | `history.append(reply["message"])` moved after the `extend` | The fake rejects it. Can they read the message? |
| Hard | `tool_call_id` hard-coded to the first call's id | Passes every single-call case. Fails on two calls. |

## Phase 4 — The limit (5 min)

Have them ask Desk: *"Find my note about the dentist and delete it."* It will say it
could not finish in one step. *"Why? What would it need?"* — a second round. *"And a
third? When does it stop?"* Leave that question open. It is Monday.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Sentence** | "No — it asks, I run it" | Correct after one follow-up | Thinks the model runs the tool |
| **Explain** | Draws the list from memory with the id | Draws it with the code open | Cannot say why the assistant turn goes back |
| **Mutate** | Names three places and fixes behaviour with words | Finds the three by running | Adds the function and stops |
| **Debug** | Reads the error as the model would | Finds it | Guesses |

Pass is 3 in every phase. **A 1 on the sentence is a fail regardless.**

---

## Say this before they leave

> **Desk can do one thing per turn. Every interesting task takes more than one. The
> fix is three lines — and three more lines to make it safe to leave alone. That is
> next week, and it is the week the course is named for.**
