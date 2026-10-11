# Week 4 — Concept fence

## Allowed

**Everything from Weeks 1–3**, plus:

- `from llm import connect, FakeModel, say, ModelError`
- `model.chat(messages, system=..., max_tokens=...)`
- The reply dictionary: `text`, `stop`, `usage`, `message`
- System prompts
- `except ModelError`, and a bare `raise` to pass an error on after cleaning up
- Asking for JSON in a prompt and validating what comes back
- Reading (Thursday onwards) the files in `llm/`

## Not yet

Tools and function calling (week 5) · the agent loop (week 6) · streaming ·
calling the `anthropic` or `openai` packages directly · embeddings, vector stores, RAG ·
fine-tuning · **any framework** — no LangChain, no LlamaIndex, nothing

---

## Why you use `llm` and not the provider's own package

Two reasons, and Thursday shows you both.

The two providers want the same information in different shapes. Code written against
one does not run against the other. `llm` is about 300 lines that hide that difference
— and on Thursday you write part of it yourself, so it is not a black box.

The second reason is tests. Everything takes a `model`, so everything can be handed a
fake one. An agent you cannot test without spending money is an agent you will not test.
