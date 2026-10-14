# Week 9 — Final defence · Project 3

One hour per student. Ten minutes of demo, then the defence. Read their `SPEC.md`,
`EVAL_REPORT.md` and `README.md` **before** they arrive.

---

## Phase 0 — Demo (10 min)

Against a real model, with the trace visible. They choose two requests; you choose
the third. Yours should be one their cut list says the agent does not do.

## Phase 1 — The paper test, again (3 min)

> *"Draw the agent loop. Then add this week's guards to the drawing."*

Same test as week 6, now with the gate, the budget and the retry on it. It should take
two minutes. If it does not, that is the finding.

## Phase 2 — Decisions (15 min)

Not *"what does this line do"*. **Why is it this way.**

1. *"You have N tools. Which one did you nearly not build? Which one did you cut?"*
2. *"Why is `X` in `DANGEROUS` and `Y` not?"* — pick the closest call.
3. *"Read me the description of your most-used tool. What did the first version say,
   and what did the model do wrong because of it?"*
4. *"Which eval case would you delete if you had to delete one? Which would you never
   delete?"*
5. *"What does your suite not test at all?"*
6. *"Your report says 7/8. Tell me about the one."*

## Phase 3 — Mutate (12 min)

- **A** — *"A second person starts using this. What changes?"* Discussion. Looking
  for: the data file, the memory, and the realisation that approval now has an
  identity problem.
- **B** — *"Add one tool, live."* You name it; it should be small and dangerous. All
  five places: function, schema, table, `DANGEROUS`, an eval case. Time it.

## Phase 4 — Attack (10 min)

Try to break it yourself, live. Use an attack that is **not** in their report. Then:
*"Whether that worked or not — what limits the damage?"*

## Phase 5 — The README (5 min)

Follow their README literally, on your machine, saying aloud what you type. Stop at
the first step that does not work.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Demo** | Narrates the trace, predicts the next step | Explains it afterwards | Surprised by its own agent |
| **Paper** | Loop and every guard in two minutes | The loop, guards when prompted | Cannot draw it |
| **Decisions** | Names what was cut and what is untested | Defends what is there | "It seemed right" |
| **Mutate** | All five places, including the eval | Function, schema, table | Function only |
| **Attack** | Points at the control that limits damage | Explains why it failed or held | Believes the prompt prevents it |
| **README** | You are running it in five minutes | Works with one question | Does not run |

Pass is 3 in every phase.

---

## Say this to every student who passes

> **You did not learn a framework. You learned what every framework is made of: a
> list that grows, a model that asks, a table that dispatches, a loop that stops, a
> gate, a budget, and a number that tells you whether it works. Whatever library you
> pick up next, you will be reading it, not trusting it.**

Then open `CUT_LIST.md` together and pick the one thing they learn next.
