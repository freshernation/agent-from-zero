# Week 8 — Friday defence

Forty minutes. The student shares `milestone/desk.py`, `attacks.py`, `THREATS.md` and
`HARDENING_REPORT.md`, and runs against a real provider.

**Open with the threat model, not the code.** Read `THREATS.md` together before
anything runs.

---

## Phase 1 — Explain (10 min)

1. *"Your gate already asks a person before sharing. Why is that not enough?"* —
   looking for: people say yes, and a share cannot be undone. The address rule comes
   before the person.
2. *"An address is not on the list. Why does your code not even ask?"* — do not offer
   a yes that must never be given.
3. *"What does 'tainted' mean, and what flips it?"* Then: *"why a fresh state every
   turn?"*
4. *"The model did exactly what the poisoned note said, and nothing was sent. What
   did you actually fix?"* — **the question of the week.** Not the model. Being
   fooled no longer matters.
5. *"What filled your window by turn ten?"* Tool results. Then: *"why can you shorten
   one and not delete it?"*
6. *"Four cases passed yesterday, five pass today, and your gate is red. Explain."*

## Phase 2 — Mutate (12 min)

- **A** — *"The user wants to share with somebody new. How do they get on the list?"*
  Discussion first. Looking for: the user adds them, in a way a note cannot — not a
  tool the model can call. A student who proposes `add_recipient` as a tool has
  rebuilt the hole.
- **B** — *"Make `remember` dangerous."* One line. Then run their suite and ask what
  it cost in questions asked. There is no free answer; watching them weigh it is the
  point.
- **C** — *"Your summary lost a title. Fix it."* Live. They should change
  `SUMMARY_SYSTEM` or `KEEP_TURNS`, and then say how they would know it worked.

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | the allowed-address check compares without lowercasing | `Sam@Example.com` is refused. Annoying, not unsafe — do they say which? |
| Medium | `watch` defines the wrapper inside the loop | Every tool calls the last one. One test names it |
| Medium | `state` is made once, outside `take_turn` | The second turn inherits the first one's taint. Nothing leaks; Desk asks about everything |
| Hard | `run_attack` does not empty the outbox | The first attack's leak is counted against all the rest |
| Nasty | `shorten_old_results` drops old tool messages instead of cutting them | The fake rejects the next call. Smaller is not the goal; legal is |

The **Nasty** one costs a student who optimised the number without reading the rule.

## Phase 4 — One live attack (8 min)

They choose an attack from `What still gets through` and run it three times against a
real model. Then: *"what would it take to stop this one, and what would that cost the
user?"*

A student whose report says nothing gets through has a suite that is too kind. Write
one more attack with them, on the spot.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Explain** | "I did not fix the model. I made being fooled not matter" | Knows the address rule is safer, cannot say why | Thinks the system prompt did it |
| **Mutate** | Keeps the list out of the model's reach | Adds the feature | Adds a tool that edits the list |
| **Debug** | Says whether each bug is unsafe or only annoying | Finds it | Guesses |
| **Attack** | Names a real remaining hole and its price | Runs the attack | Claims nothing gets through |
