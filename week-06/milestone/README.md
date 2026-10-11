# Week 6 Milestone — Project 2: an agent, from scratch

> A working agent with no framework under it, and a page explaining how it works in
> your own words.

This is the keystone of the course. Everything from here on is added to this file.

---

## The files

| File | Where it comes from |
|---|---|
| `kit.py` | given |
| `guards.py` | **copy from day 3** |
| `show.py` | **copy from day 2** |
| `agent.py` | **copy from day 3** — this is the finished `run_agent` |
| `cli.py` | new |
| `WRITEUP.md` | new — yours to write |

## `cli.py`

### `SYSTEM`

Your system prompt for Desk. At least 30 words. It should say who Desk is, that it
must use its tools rather than guess, and how to behave when a tool reports an error.

### `answer_task(model, task)` → the text to show the user

Runs the agent on one task with `SYSTEM`, `kit.SCHEMAS` and `kit.TOOLS`, and returns
two lines:

```
Saved. That is 17400 a year.
(done in 3 steps (300 tokens in, 60 out))
```

The second line is `summary(result)` in brackets.

If the environment variable `AGENT_TRACE` is `"1"`, the formatted trace comes first,
then a blank line, then those two lines.

### `main()`

`connect()`; loop on the prompt `Task: `; print what `answer_task` returns; on `quit`
print `Bye.` Behind the `__name__` guard.

Each task is a fresh run of the agent. The notes file is what carries over between
tasks — the conversation does not. (Carrying the conversation is next week.)

---

## `WRITEUP.md`

A template is in this folder. Fill in every section. **Write it yourself** — it is the
one file in this course where the words matter more than the code, and on Friday you
will read it out loud.

It must include one real trace from a real model, pasted in, with your explanation of
each line.

---

## Check it

```bash
pytest week-06/milestone -v
AGENT_TRACE=1 python3 week-06/milestone/cli.py
```

Give it hard things, against a real provider:

- *"Add notes for milk, eggs and bread, then delete the eggs one, then tell me what is left."*
- *"What is 15% of the total of 1450, 60 and 85?"*
- *"Delete the note about my car."* (when there is none)

Read the trace every time. When it does something you did not expect, work out
**which tool result** it was reasoning from.

---

## Then make it good

- [ ] You can draw the loop on paper in ninety seconds, including the exits.
- [ ] You can name all six values of `stopped` and say what causes each.
- [ ] You have made your agent hit **each** of them at least once, on purpose.
- [ ] Your write-up contains no sentence you could not defend.

---

## Friday

The most important defence in the course. It starts on paper.
