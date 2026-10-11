# Week 6 — Concept fence

## Allowed

**Everything from Weeks 1–5**, plus:

- A `while` loop around `model.chat`
- A result dictionary describing how a run ended
- `json.dumps(args, sort_keys=True)` to compare two calls
- Slicing a string: `text[:2000]`

## Not yet

**Any framework.** No LangChain, no LangGraph, no CrewAI, no AutoGen, no `smolagents`,
no OpenAI Agents SDK, no Claude Agent SDK, no SDK "tool runner". Not one. ·
Multi-agent anything · planners · vector stores · MCP · running tools in parallel ·
long-term memory (week 7) · approval gates (week 7)

---

## Why the fence is absolute this week

Everything you build this week has a library that will do it for you in four lines.
You will meet those libraries after this course and they will feel obvious — *because
you will have already written what they hide*.

A student who reaches for a framework now saves three days and loses the only chance
they will ever get to understand what an agent actually is.

It is also the difference in an interview. Everybody has used an agent framework.
Almost nobody can draw the loop on a whiteboard.

If an AI offers you a framework this week, tell it no. That is what the fence in
`ai/tutor.md` is for.
