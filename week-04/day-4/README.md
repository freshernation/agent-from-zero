# Day 4 — Open the box

> **By the end of today** you can read the request each provider actually receives, and
> you have written the translation yourself.

All week you called `model.chat(...)` and got a tidy dictionary back. Today you look at
what was underneath. There is no magic in there — just two companies that chose
different names for the same things.

---

## Read first

- [ ] Claude — [Messages API reference](https://platform.claude.com/docs/en/api/messages) — the request body and the response · 15 min
- [ ] OpenAI — [Chat Completions API reference](https://developers.openai.com/api/reference/resources/chat) — the request body and the response · 15 min
- [ ] `llm/wire.py` in this repo — **after** you finish the exercises, not before

---

## What you need to know

### The same question, twice

What you write:

```python
model.chat([{"role": "user", "content": "Capital of Peru?"}], system="One word.")
```

What Claude is sent:

```json
{
  "model": "claude-opus-5-5",
  "max_tokens": 1024,
  "system": "One word.",
  "messages": [{"role": "user", "content": "Capital of Peru?"}]
}
```

What OpenAI is sent:

```json
{
  "model": "gpt-5-mini",
  "messages": [
    {"role": "system", "content": "One word."},
    {"role": "user", "content": "Capital of Peru?"}
  ]
}
```

One real difference: for Claude the system prompt is its own field; for OpenAI it is
the first message in the list.

### The same answer, twice

Claude replies:

```json
{
  "content": [
    {"type": "thinking", "thinking": "", "signature": "EqQB..."},
    {"type": "text", "text": "Lima."}
  ],
  "stop_reason": "end_turn",
  "usage": {"input_tokens": 14, "output_tokens": 3}
}
```

OpenAI replies:

```json
{
  "choices": [
    {"message": {"role": "assistant", "content": "Lima."}, "finish_reason": "stop"}
  ],
  "usage": {"prompt_tokens": 14, "completion_tokens": 3}
}
```

| | Claude | OpenAI | `llm` calls it |
|---|---|---|---|
| The text | `content` — a **list of blocks**; join the `text` ones | `choices[0].message.content` — a string, or `null` | `reply["text"]` |
| Finished normally | `stop_reason: "end_turn"` | `finish_reason: "stop"` | `"done"` |
| Ran out of room | `"max_tokens"` | `"length"` | `"length"` |
| Declined | `"refusal"` | `"content_filter"` | `"refused"` |
| Tokens in / out | `input_tokens` / `output_tokens` | `prompt_tokens` / `completion_tokens` | `usage["input"]` / `["output"]` |

Claude's `content` being a list matters. A reply can hold several blocks, and not all
of them are text — you must check each block's `type`. Next week a third type appears
in that list and it is the reason this course exists.

### That is what an adapter is

A function that turns one shape into another. `llm/wire.py` is nothing else. Once you
have written today's exercises you have written a third of it.

---

## Exercises

```bash
pytest week-04/day-4 -v
```

All in `dialects.py`. Everything here is plain dictionaries — no network, no model.

| Function | Returns |
|---|---|
| `claude_request(model_name, messages, system=None, max_tokens=1024)` | the request body above. Leave `"system"` out entirely when there is none |
| `openai_request(model_name, messages, system=None)` | the request body above, with the system prompt as the first message when there is one. Must not change the `messages` list it was given |
| `claude_text(raw)` | the text of a Claude response: every `text` block, joined |
| `openai_text(raw)` | the text of an OpenAI response; `""` when the content is `None` |
| `neutral_stop(provider, raw)` | `"done"`, `"length"` or `"refused"`. `provider` is `"claude"` or `"openai"`. Anything you do not recognise is `"done"` |
| `neutral_usage(provider, raw)` | `{"input": ..., "output": ...}` |

When all six pass, open `llm/wire.py` and read `claude_reply` and `openai_reply`. You
should recognise every line.

---

## Predict-then-run

Before you read it: `llm/wire.py` has to translate in **both** directions for
messages but only **one** direction for replies. Why?

---

## Before you close the laptop

Commit, push, fill in the signal log.
