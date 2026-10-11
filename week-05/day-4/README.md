# Day 4 — Open the box, again

> **By the end of today** you can read a tool call in each provider's own format, and
> you have written the translation.

Same exercise as last Thursday, one layer deeper. Tool use is where the two providers
differ most — and where, if you ever debug a real agent, you will be reading raw JSON.

---

## Read first

- [ ] Claude — [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) — the JSON examples · 10 min
- [ ] OpenAI — [Function calling](https://platform.openai.com/docs/guides/function-calling) — the JSON examples · 10 min
- [ ] `llm/wire.py` — **after** the exercises

---

## What you need to know

### The schema

Yours, Claude's, OpenAI's:

```python
{"name": "calculate", "description": "...", "parameters": {...}}

{"name": "calculate", "description": "...", "input_schema": {...}}

{"type": "function",
 "function": {"name": "calculate", "description": "...", "parameters": {...}}}
```

Same three facts. One renames a key; the other wraps them one level deeper.

### The model asking for a tool

Claude puts the request in the `content` list, as a block of type `tool_use`:

```json
{
  "content": [
    {"type": "text", "text": "Let me work that out."},
    {"type": "tool_use", "id": "toolu_01A", "name": "calculate",
     "input": {"expression": "17 * 23"}}
  ],
  "stop_reason": "tool_use"
}
```

OpenAI puts it beside the content, in its own `tool_calls` list:

```json
{
  "choices": [{
    "message": {
      "content": null,
      "tool_calls": [
        {"id": "call_abc", "type": "function",
         "function": {"name": "calculate", "arguments": "{\"expression\": \"17 * 23\"}"}}
      ]
    },
    "finish_reason": "tool_calls"
  }]
}
```

Look hard at `arguments` in the second one. It is **a string containing JSON**, not a
dictionary. You must `json.loads` it — and it can fail to parse, because a model wrote
it. Claude's `input` arrives already parsed.

### Sending the result back

Claude has no `tool` role. Results travel inside a **user** message, as `tool_result`
blocks, and several results must share **one** message:

```json
{"role": "user", "content": [
  {"type": "tool_result", "tool_use_id": "toolu_01A", "content": "391"},
  {"type": "tool_result", "tool_use_id": "toolu_01B", "content": "Saved 'milk'."}
]}
```

OpenAI has a `tool` role, with one message per result:

```json
{"role": "tool", "tool_call_id": "call_abc", "content": "391"}
```

That second shape should look familiar. The course's neutral format borrowed it.

| | Claude | OpenAI |
|---|---|---|
| Schema key | `input_schema` | `function.parameters` |
| Where the request is | a `tool_use` block in `content` | `message.tool_calls` |
| Arguments | `input` — a dict | `function.arguments` — a JSON **string** |
| Stop value | `tool_use` | `tool_calls` |
| Result | `tool_result` blocks in one **user** message | one `tool` message each |
| The id field on a result | `tool_use_id` | `tool_call_id` |

---

## Exercises

```bash
pytest week-05/day-4 -v
```

All in `tool_dialects.py`. Plain dictionaries; no model.

| Function | Returns |
|---|---|
| `claude_tool(schema)` | the schema in Claude's shape |
| `openai_tool(schema)` | the schema in OpenAI's shape |
| `claude_calls(raw)` | neutral calls — `[{"id", "name", "args"}]` — from a raw Claude response. `[]` if there are none |
| `openai_calls(raw)` | the same from a raw OpenAI response. `tool_calls` may be missing or `None`. Arguments that will not parse become `{}` |
| `claude_results(tool_messages)` | **one** Claude user message carrying all of the neutral `tool` messages |
| `openai_results(tool_messages)` | a list of OpenAI `tool` messages |

Then read `llm/wire.py` top to bottom. It should now be boring.

---

## Predict-then-run

The model writes `"arguments": "{\"expression\": \"17 * 23\""` — note the missing
closing brace. What should an agent do? Crash, skip the call, or run the tool with no
arguments and let the error message go back? Argue for one. (`llm/wire.py` made a
choice; see if you agree.)

---

## Before you close the laptop

Commit, push, fill in the signal log.
