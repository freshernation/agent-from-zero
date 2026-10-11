# Day 2 — What does it know?

> **By the end of today** your agent can carry a conversation across tasks, cut that
> conversation without corrupting it, and remember a fact for next week.

"Memory" in an agent means three different things. People mix them up constantly.

| | Lives in | Lasts | Today's name for it |
|---|---|---|---|
| **The conversation** | the message list | until you cut it | history |
| **What it is working on** | the same list, this run | one run | (the loop — you have this) |
| **Facts it should keep** | a file | until deleted | long-term memory |

---

## Read first

- [ ] Anthropic — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · 25 min
- [ ] Claude — [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) · 10 min

---

## What you need to know

### 1. Carrying the conversation

Last week every task started from an empty list, so *"delete that one"* meant nothing.
The fix is week 4 again: keep the list, and start the next run from it.

```python
result = run_agent(model, "Add a note about the dentist", ..., history=history)
if result["stopped"] == "done":
    history = result["messages"]
```

**Only carry a run forward if it ended with `done`.** A run that was stopped early
can end with tool calls that were never answered. Feed that back in and the next
request is rejected. Keep the old history instead.

### 2. It cannot grow forever

Every step resends the whole list. A model has a maximum it can read (its **context
window**), you pay for every token in it on every step, and models get worse at
finding things in a very long conversation well before they hit the limit.

A rough size, good enough to decide when to cut: **four characters is about one
token.**

### 3. Cutting without corrupting

You cannot just drop the oldest ten messages. Three rules, all of which a real API
enforces:

- The list must still **start with a user message**.
- A tool result must never be separated from the assistant turn that asked for it.
- An assistant turn with tool calls must keep **all** its results.

The safe unit to cut is a **turn**: one user message and everything after it up to
the next user message. Keep the last *N* whole turns and every rule holds
automatically.

### 4. Private keys do not survive a cut

Some providers attach their own data to an assistant message — you have seen it as the
`"_raw"` key. It is only valid for the exact conversation that produced it. Once you
have cut earlier turns, it no longer matches, and the provider may reject it.

So when you cut, give back **copies** of the kept messages with every key starting
with `_` removed. When you cut nothing, change nothing.

### 5. Long-term memory is just a tool and a file

There is no special memory system in an agent. There is a `remember` tool that appends
a line to a file, and a `recall` tool that reads it back. The model decides when to
use them, the same way it decides when to use `calculate` — which means, once again,
that the **descriptions** decide how good the memory is.

To give an agent extra tools, combine the lists and the tables:

```python
schemas = SCHEMAS + MEMORY_SCHEMAS

tools = dict(TOOLS)              # a copy
tools.update(MEMORY_TOOLS)       # add the memory tools to the copy
```

---

## Exercises

```bash
pytest week-07/day-2 -v
```

### 1. `memory.py`

| Name | What it is |
|---|---|
| `estimate_tokens(messages)` | the total number of characters in every `content`, divided by 4, as a whole number |
| `trim(messages, max_turns)` | the last `max_turns` turns. If nothing needs cutting, return a list with the same messages, untouched. If something is cut, return **copies** of the kept messages without any key starting with `_`. Never changes its input |
| `carry(history, result, max_turns=10)` | the history to use next: the trimmed `result["messages"]` if the run ended `done`, otherwise `history` unchanged |
| `remember(fact)` | saves the fact to the JSON list in the file named by `MEMORY_FILE` (default `memory.json`). Returns `Remembered.`, or `I already know that.` for an exact repeat |
| `recall(word="")` | the facts containing the word, any capitals, one per line. With no word, all of them. `Nothing remembered yet.` or `Nothing remembered about 'x'.` when there is nothing to show |
| `MEMORY_SCHEMAS` | two schemas, for `remember` and `recall`, descriptions of ten words or more |
| `MEMORY_TOOLS` | the dispatch table for those two |

### 2. `agent.py`

Copy yesterday's `agent.py`, `guards.py` and `gate.py` here. Add one argument:

```python
run_agent(..., history=None)
```

When `history` is given, the run starts from a **copy** of it with the task appended.
The caller's list must not change.

---

## Predict-then-run

With a real provider: tell the agent your name and one preference, with the memory
tools on. Delete your `history`. Start a new run and ask what it knows about you.
Did it call `recall`? If not — what does your description of `recall` say about
*when* to use it?

---

## Before you close the laptop

Commit, push, fill in the signal log.
