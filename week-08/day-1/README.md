# Day 1 — What is in the window?

> **By the end of today** you can say what is filling your agent's conversation, and
> shrink it without losing what matters or breaking the rules of the API.

Week 7's answer to a long conversation was to drop the oldest turns. That works, and
it forgets. Today you find out what is actually taking up the room, and you get two
better tools than deletion.

---

## Read first

- [ ] Anthropic — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · 25 min
- [ ] Claude — [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) · 10 min

---

## What you need to know

### 1. Measure before you cut

You already have an estimate: four characters is about one token. Add it up **by
role** and look.

```python
sizes(messages)
# {"user": 20, "assistant": 31, "tool": 508, "total": 559}
```

That is a real shape. The user typed three short sentences. One `find_notes` came back
with two thousand characters. The window is not full of conversation. It is full of
**tool results**, and most of them were only needed for the step that asked for them.

After every real model call you also get the true number, for free:
`reply["usage"]["input"]` is exactly how many tokens you just sent. The estimate is
for deciding in advance. The usage is for checking you were right.

### 1b. Count what is really sent, before you send it

`sizes` counts the conversation. A request carries more: the system prompt, and every
tool description, on every call. Desk's six tool descriptions come to **565 tokens** —
more than the whole conversation above — and `sizes` sees none of them.

Both providers will count a request for you before you send it, for free: Claude's
`messages.count_tokens`, OpenAI's `responses.input_tokens.count`. The course's models
expose it as `model.count_tokens(messages, system=..., tools=...)`, and the fake one
counts every character it would send, divided by four. Use the provider's number when
you can, and fall back to your estimate — of **everything** sent — when the counter is
unreachable.

### 2. Shorten old results. Never drop them

A search result from ten steps ago has done its job. Keep the first two hundred
characters and say what you did:

```
milk: two litres, eggs: six, bread: one loaf ... [shortened: 1800 characters removed]
```

**You may not delete the message.** The model asked for that tool, and every API
insists that a request for a tool is followed by its result. Cut the content; keep
the message, its `role` and its `tool_call_id`.

Leave the last couple of results alone. The model is probably still using them.

### 3. Summarise instead of forgetting

`trim` throws away the oldest turns. The alternative is to ask a model to write down
what happened in them, and keep that instead.

```python
summary = summarise(model, older_messages)     # one extra model call
```

Then the first message of what you kept starts with it:

```
Summary of the conversation so far: The user saved a note called 'dentist'
and asked what they had saved about work.

Delete the dentist note.
```

Three things to get right:

- **Say what must survive.** A summariser left alone keeps the gist and loses the
  exact title, and `delete_note` needs the exact title. Your `SUMMARY_SYSTEM` is a
  prompt like any other, and it is the whole quality of the memory.
- **Keep the recent turns whole.** Summarise the old ones only.
- **Do not summarise what is short.** A summary costs a model call. Three turns do
  not need one.

### 4. It is a second model call, inside your code

`summarise` calls `model.chat` itself, with its own system prompt and no tools. That
is new: until now only the loop talked to the model. It means a summary can be wrong
in ways your agent never sees — and on Friday you will go looking.

---

## Exercises

```bash
pytest week-08/day-1 -v
```

Write `context.py`:

| Name | What it is |
|---|---|
| `tokens(text)` | `len(text) // 4` |
| `sizes(messages)` | estimated tokens for `user`, `assistant`, `tool` and `total` |
| `shorten_old_results(messages, keep_last=2, limit=200)` | a new list of copies; every tool result except the last `keep_last` is cut to `limit` characters, then ` [shortened: N characters removed]`. Nothing is dropped and nothing else changes |
| `split_turns(messages)` | a list of turns; a turn starts at each user message |
| `SUMMARY_SYSTEM` | the summariser's instructions, 30 words or more, saying what must survive — titles among it |
| `transcript(messages)` | one line per message, `role: content` |
| `summarise(model, messages)` | one model call — the transcript as a single user message, `system=SUMMARY_SYSTEM`, no tools — and its text |
| `compact(model, messages, keep_turns=3)` | no more than `keep_turns` turns: a copy, and no model call. Otherwise the kept turns as copies, without keys starting `_`, with `Summary of the conversation so far: <summary>` and a blank line put in front of the first kept message's content |
| `should_compact(used, window, fraction=0.5)` | `True` when `used` is at least that fraction of the window |
| `tools_size(tools)` | `len(json.dumps(tools)) // 4`, 0 for none |
| `estimate(messages, system=None, tools=None)` | the conversation, the system prompt and the tool descriptions, together |
| `window_used(model, messages, system=None, tools=None)` | `{"tokens", "source"}`: the provider's count when it answers, your estimate when it does not |

---

## Predict-then-run

With a real provider, hold a ten-turn conversation with last week's Desk in which
turn one saves a note with an unusual title. Print `sizes(history)` after every turn.

Predict two things first: which role will be biggest by turn ten, and whether a
summary of the first seven turns will still contain that title, spelled exactly.

---

## Before you close the laptop

Commit, push, fill in the signal log.
