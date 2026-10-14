# Day 2 — What can leave?

> **By the end of today** a note cannot be sent to an address nobody chose — whatever
> the model asks for, and whatever the person at the keyboard says.

Open `kit.py`. There is a sixth tool: `share_note(title, to)`.

Last week a poisoned note could try to delete things, and the approval gate stopped
it. Today a poisoned note can try to send your bank details to a stranger. The gate
is still there. It is not enough, and working out why is the day.

---

## Read first

- [ ] Simon Willison — [The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) · 15 min
- [ ] OWASP — [LLM06: Excessive agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) · 10 min

---

## What you need to know

### 1. Why asking a person is not enough

Put `share_note` in `dangerous` and the user is asked:

```
Allow share_note({"title": "bank", "to": "help@desk-support.example"})? [y/N]
```

A careful person says no. But this is the fortieth question today, the address looks
plausible, and they asked Desk for their reminders a second ago. People say yes.

For a delete, a wrong yes loses a note. For a share, it is gone and cannot be called
back. So for this tool there is a rule that comes **before** the person.

### 2. Check the argument, not just the tool

Week 7's gate looks at the tool's **name**. Today's looks at what it was aimed at.

```python
ALLOWED = {"sam@example.com", "me@example.com"}

allowed_recipient("help@desk-support.example", ALLOWED)   # False
```

An address that is not on the list is refused, and **the person is never asked**. Do
not offer somebody a yes that must never be given.

The list is short and you wrote it. That is the point. The model cannot add to it and
a note cannot talk its way onto it.

### 3. Three things that must not meet

An agent is dangerous when, in one run, it has all three of:

1. **private things** — your notes
2. **text a stranger wrote** — a note pasted from an email, a memory planted last week
3. **a way out** — `share_note`

Desk has the first and the third all the time. The second arrives the moment a tool
returns stored text. So watch for that moment.

```python
state = {"tainted": False}
tools = watch(TOOLS, {"find_notes", "list_titles"}, state)
```

`watch` gives back the same tools, each wrapped so that calling a **reader** flips
`state["tainted"]` to `True`. From then on in that run, even an allowed address needs
a person to say yes.

| | Not tainted | Tainted |
|---|---|---|
| address not on the list | refused | refused |
| address on the list | goes through | **ask a person** |

### 4. A function that builds a function

`run_agent` calls `approve(call)` with one argument. But today's rule needs to know
the allowed list and the state as well. So you write a function that **makes** the
approver, with those two things remembered inside it:

```python
def make_approver(allowed, state, ask=None):
    def approve(call):
        ...            # can use allowed, state and ask
    return approve
```

The inner function is created fresh each time `make_approver` runs, and it keeps
hold of the values it was made with. Note that it reads `state["tainted"]` when it is
**called**, not when it is made — so it sees what happened earlier in the run.

`watch` needs the same trick once per tool, and there is a trap in it. Write the
wrapper in a helper of its own:

```python
def watched(function, name, readers, state):
    def run(**args):
        ...
    return run
```

and call that helper inside your loop. If you define `run` directly inside the loop
instead, every wrapper ends up calling the **last** tool in the table. There is a
test with that bug's name on it.

---

## Exercises

```bash
pytest week-08/day-2 -v
```

Copy `agent.py`, `guards.py` and `retry.py` from your week 7 milestone. Then write
`leak.py`:

| Name | What it does |
|---|---|
| `allowed_recipient(to, allowed)` | `True` when the address is on the list, ignoring capitals and surrounding spaces |
| `watched(function, name, readers, state)` | returns a function that, when called, sets `state["tainted"] = True` if `name` is in `readers`, then calls `function` with the same arguments |
| `watch(tools, readers, state)` | a new dispatch table with every tool watched. The original is untouched |
| `make_approver(allowed, state, ask=None)` | returns `approve(call)` |

The approver's rules:

| The call | What `approve` returns |
|---|---|
| `share_note` to an address **not** allowed | `False`, without asking |
| `share_note` to an allowed address, run **not** tainted | `True`, without asking |
| anything else | `ask(call) is True` — and `False` when `ask` is `None` |

---

## Predict-then-run

Put the poisoned reminder from the tests in a real notes file. Run last week's Desk
against a real provider and ask *"Do I have any reminders?"* five times, with
`share_note` offered and no gate on it. Then look at the outbox.

Predict the count before you run it. Then run today's version five times.

---

## Before you close the laptop

Commit, push, fill in the signal log.
