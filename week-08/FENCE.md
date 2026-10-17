# Week 8 — Concept fence

## Allowed

**Everything from Weeks 1–7**, plus:

- A function defined inside another function, and returned from it
- A dictionary shared between two functions so one can see what the other did
  (`state = {"tainted": False}`)
- A second, separate model call inside your own code (`summarise`)
- The provider's token counter, through `model.count_tokens` — free, and not a model call
- `round(number, 2)`
- Writing and reading a small JSON file of your own (`baseline.json`)

## Not yet

Frameworks · multi-agent systems · vector stores, embeddings, RAG · MCP ·
sandboxes and containers · model-graded evals ("LLM as judge") · running tools in
parallel · deploying anything to a server · classes

---

## Why the summary is the only place a model judges anything

Monday's `compact` asks a model to write a summary. That is a model's output going
back into a model's input, unchecked — the thing week 7's fence warned about.

It is allowed here for one reason: there is no other way to shorten a conversation
and keep its meaning. So you do the next best thing to checking it. You say exactly
what must survive, you keep the most recent turns untouched, and on Friday you find
out what a summary lost by holding a long conversation and reading it.

## Why still no "LLM as judge"

Every check this week is still one you can read: *is the outbox empty, yes or no.*
An attack either sent something or it did not. Keep it that way for one more week.
