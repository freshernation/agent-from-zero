# Week 4 — Friday defence

Thirty minutes. The student shares `milestone/assistant.py` and runs it against a
**real** provider for part of this.

---

## Phase 0 — Live (3 min)

Have them tell Desk their name, chat for two turns, ask for the name back, `/reset`,
and ask again. Then: *"Where was your name stored between those messages?"* The only
right answer points at a line in their file.

## Phase 1 — Explain (7 min)

1. *"The model answered 'Sam' on the second turn. Did it remember?"* — **no**, and then
   *"so what happened?"*
2. *"Why do you append `reply["message"]` rather than build a dict from `reply["text"]`?"*
3. *"The system prompt — is it in `history`? Where does it go, and how often is it sent?"*
4. *"Turn ten of a chat. Roughly how many messages does that one call send? Who pays?"*
5. *"What is `stop` when a reply is cut off, and what would your user have seen if you
   had never checked it?"*

## Phase 2 — Mutate (10 min)

- **A** — *"Add `/system <text>`, which replaces the system prompt mid-conversation."*
  Where does it live in the session? Does the model see the old one again? (No — it is
  sent fresh each call.)
- **B** — *"Refuse to send once the session has cost more than five cents."* Which
  function, which line, what does the user see? Looking for: the check goes **before**
  the call, and the meter was already there to make it possible.

## Phase 3 — Debug (7 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | `history.append(reply["message"])` deleted | Second turn: the fake rejects two user messages in a row. Can they read that message? |
| Medium | `history.pop()` deleted from the error path | Works until one failure, then every later call is rejected |
| Hard | usage added **before** the `ModelError` check, from a stale variable | Meter drifts. Nothing fails. |

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Live** | "In my list — the model was sent it again" | Gets there with a prompt | "It remembered" |
| **Explain** | Explains cost growth unprompted | Correct when asked | Thinks the provider stores the chat |
| **Mutate** | Places the budget check before the call | Places it after, then sees why not | Cannot locate the call |
| **Debug** | Reads the fake's message and goes to the line | Finds it by experiment | Guesses |

Pass is 3 in every phase. **A 1 on the live phase is a fail regardless** — a student
who believes the model remembers will not be able to build next week's loop.

---

## Say this before they leave

> **You have a loop, a model, and a list that grows. One thing is missing: the model
> can only talk. Next week it gets hands.**
