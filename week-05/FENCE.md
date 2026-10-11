# Week 5 — Concept fence

## Allowed

**Everything from Weeks 1–4**, plus:

- Tool schemas as plain dictionaries (JSON Schema: `type`, `properties`, `required`)
- `model.chat(messages, tools=schemas)`
- `reply["stop"] == "tools"` and `reply["tool_calls"]`
- `{"role": "tool", "tool_call_id": ..., "content": ...}` messages
- A dispatch table — a dictionary mapping names to functions
- `function(**args)` to unpack a dictionary into keyword arguments
- `except Exception as error` — **only** at the one place where you run a tool you do
  not control
- `from llm import use, use_many` in your own experiments

## Not yet

**A loop around the model.** One round of tools per question, this week. If the model
wants a second round, you tell the user you could not finish. That limit is deliberate
and next week removes it. · Any framework · MCP · parallel execution · streaming

---

## Why only one round

Because the loop is the whole of next week, and it deserves a week. If you write
`while` around a model call this week you will get something that works on the happy
path and spends money forever on the unhappy one — and you will not yet have the three
guards that make a loop safe to leave alone.
