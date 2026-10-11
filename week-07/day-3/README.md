# Day 3 — How do you know it works?

> **By the end of today** you can state, as a number, how often your agent does the
> right thing — and re-measure it after every change.

*"It worked when I tried it"* is not evidence. The model is different every run, and
you only tried the things you thought of. An **eval** is a task with an outcome you
can check automatically. A set of them is the only honest answer to *"is the agent
better or worse than yesterday?"*

---

## Read first

- [ ] Anthropic — [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) · 30 min
- [ ] Claude — [Define your success criteria](https://platform.claude.com/docs/en/test-and-evaluate/define-success) and [Develop test cases](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) · 20 min

---

## What you need to know

### A case

```python
{
    "name": "delete one of three",
    "notes": [{"title": "milk", "body": ""}, {"title": "eggs", "body": ""}],   # starting state
    "task": "Delete the eggs note.",
    "expect": {
        "stopped": "done",
        "titles": ["milk"],                 # what should be left
        "calls": ["delete_note"],           # tools that must have been used
        "never_calls": ["add_note"],        # tools that must not
        "max_steps": 4,
        "answer_contains": "eggs",
    },
}
```

Every key in `expect` is optional. A case checks only what it names.

### Check the outcome first, the path second, the words last

In order of how much to trust them:

1. **The state of the world.** Is `eggs` gone and `milk` still there? This is the
   strongest check there is. It does not care how the agent got there.
2. **The trajectory.** Did it call `delete_note`? Did it stay under four steps? Did it
   leave `add_note` alone? Useful, but there are often several correct paths — do not
   over-specify.
3. **The wording.** `answer_contains` is the weakest check. Models rephrase. Use it
   for a number or a name, never for a sentence.

### Every case starts clean

A case that depends on what the previous case left behind is not a test, it is a
coincidence. Write the starting notes before each run.

### Write the cases you are afraid of

Six cases that all pass tell you nothing. Good suites include:

- the plain happy path,
- a task that needs **several** steps,
- a task that is **impossible** (delete a note that does not exist) — the right
  outcome is that nothing changes and it says so,
- a task where a tool must **not** be used,
- an **injected** instruction, with the gate on, expecting no damage,
- an ambiguous request, to see what it does.

### One run is an anecdote

Against a real model, the same case can pass four times in five. Run each case
several times and report a rate. *"5/6 cases, each 3 runs out of 3"* is a result.
*"It passed"* is a mood.

---

## Exercises

```bash
pytest week-07/day-3 -v
```

Copy `agent.py` and `guards.py` from day 2. Then write `evals.py`:

| Function | Returns |
|---|---|
| `tools_called(result)` | the names of the tools the model asked for, in order, from the trace |
| `check(result, expect, titles)` | a list of failure sentences — empty means pass. `titles` is the list of note titles after the run |
| `run_case(model, case, schemas, tools, system=None, dangerous=None, approve=None)` | writes the case's starting `notes` (or `[]`) to the notes file, runs the agent, and returns `{"name", "passed", "failures", "steps"}` |
| `report(outcomes)` | one line per outcome, then the score |

The failure sentences, in this order, when the matching key is in `expect`:

| Key | Sentence when it fails |
|---|---|
| `stopped` | `stopped: expected 'done', got 'max_steps'` |
| `answer_contains` | `answer does not contain '17400'` — ignoring capitals |
| `calls` | `did not call calculate` — one sentence per missing tool |
| `never_calls` | `called delete_note` — one per forbidden tool that was used |
| `max_steps` | `took 7 steps, more than 4` |
| `titles` | `notes: expected ['milk'], got ['eggs', 'milk']` — both sorted, order does not matter |

The report:

```
PASS add a note
FAIL delete one of three: did not call delete_note; notes: expected ['milk'], got ['eggs', 'milk']
1/2 passed
```

The notes file is `os.environ.get("NOTES_FILE", "notes.json")`.

Then run `python3 week-07/day-3/try_evals.py` against a real provider. It is given,
with five cases. It uses its own notes file, so your real notes are safe.

---

## Predict-then-run

Before running `try_evals.py`, read its five cases and predict which one a real model
is most likely to fail. Run it three times. Were you right?

---

## Before you close the laptop

Commit, push, fill in the signal log.
