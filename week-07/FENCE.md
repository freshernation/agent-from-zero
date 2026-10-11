# Week 7 — Concept fence

## Allowed

**Everything from Weeks 1–6**, plus:

- Passing a function as an argument (`approve=...`, `wait=...`, `ask=input`)
- `time.sleep`, and `2 ** attempt` for a growing delay
- Sets: `{"delete_note"}` and `name in dangerous`
- Copying a dictionary: `dict(message)`; copying a list: `list(messages)`
- `ModelError.retryable`

## Not yet

Frameworks · multi-agent systems · vector stores, embeddings, RAG · MCP ·
sandboxes and containers · model-graded evals ("LLM as judge") · running tools in
parallel · deploying anything to a server

---

## Why no model-graded evals

Asking a second model whether the first one did well is a real technique and you will
meet it. But it is a second non-deterministic thing judging the first, and it is easy
to build a judge that agrees with whatever it is shown. This week every check is one
you can read: *did the note get deleted, yes or no.* Learn to write those first — most
people who reach for a judge model did not need one.
