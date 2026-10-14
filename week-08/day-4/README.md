# Day 4 — Evals that hold the line

> **By the end of today** your evals check which note a tool was aimed at, a failed run
> becomes a case you keep, and a change that breaks something cannot slip past a
> better score.

Week 7's evals have two holes. Both are easy to fall through and both are small to
close.

---

## Read first

- [ ] Anthropic — [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — the part on regression evals · 15 min
- [ ] Claude — [Develop test cases](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) · 10 min

---

## What you need to know

### Hole 1 — the right tool, aimed at the wrong thing

```python
"expect": {"calls": ["delete_note"]}
```

The user asked to delete `eggs`. The agent deleted `milk`. `delete_note` was called,
so that check passes.

Week 7 would have caught this one through `titles`, because the wrong note is
missing. But `share_note` changes nothing in the notes file. Send the bank note to
the wrong person and every check you own is green.

So check the arguments:

```python
check_args(result, {"share_note": {"to": "sam@example.com"}})
# ["share_note: to expected 'sam@example.com', got 'x@example.org'"]
```

A tool passes if **any one** of its calls has every argument you named. The model
may look twice before it finds the right note, and that is fine. Arguments you did
not name do not matter.

### A failed run is a case you have not written yet

Something goes wrong against a real model. You find the cause and fix it. Next month
somebody changes a tool description and it comes back.

Unless, the moment it was fixed, you turned the working run into a case:

```python
case = freeze("delete eggs", "Delete the eggs note.", notes, result, titles)
```

`freeze` records how the run stopped, which tools it used, and what was left. Paste
that into your cases. The bug now has a test with its name on it.

### Hole 2 — the score went up and something broke

Yesterday: 3 of 4 cases passed. You change the system prompt. Today: 4 of 5.

Better? Look closer. You added a case, it passes, a case that was failing now passes
— and one that **worked yesterday fails today**. The score cannot show you that. It
went up.

So keep a **baseline**: which cases passed, by name.

```python
save_baseline("baseline.json", outcomes)
...
gate(load_baseline("baseline.json"), new_outcomes)
# {"ok": False, "regressions": ["delete one of three"], "new": ["share when asked"],
#  "before": "3/4", "after": "4/5"}
```

A **regression** is a case that passed in the baseline and fails now. Nothing else
is one:

- a case that was already failing is still a problem, and not one this change caused
- a new case has nothing to regress from

The gate fails on regressions and on nothing else. When a regression is on purpose —
you changed what the right answer is — fix the case, save a new baseline, and write
down why. That is a decision. A red gate you ignore is not.

### Flaky is not broken

A real model passes some cases four times in five. If one unlucky run can turn your
gate red, people stop believing it within a week. So against a real model, run each
case several times and call it passed only when it passes most of them — then feed
*that* to the gate.

---

## Exercises

```bash
pytest week-08/day-4 -v
```

Write `baseline.py`. It needs nothing copied: every function works on results and
outcomes you already know the shape of.

| Name | What it does |
|---|---|
| `called_with(result)` | every tool call with its arguments, in order: `[{"name", "args"}, ...]` |
| `check_args(result, expected)` | failure sentences; `[]` means pass |
| `freeze(name, task, notes, result, titles)` | an eval case pinning down what the run did |
| `save_baseline(path, outcomes)` | writes `{"case name": true/false}` as JSON |
| `load_baseline(path)` | reads it back; `{}` when there is no file |
| `regressions(baseline, outcomes)` | names that passed before and fail now, in the order of `outcomes` |
| `gate(baseline, outcomes)` | `{"ok", "regressions", "new", "before", "after"}` |
| `exit_code(result)` | `0` when ok, `1` when not |

`check_args` sentences, for each tool in `expected`:

| Situation | Sentence |
|---|---|
| the tool was never called | `did not call delete_note` |
| called, but no call has every expected argument | `delete_note: title expected 'eggs', got 'milk'` — one per wrong argument of the **last** call; a missing argument is `None` |

`freeze` returns:

```python
{"name": name, "task": task, "notes": notes,
 "expect": {"stopped": ..., "calls": [each tool once, in first-use order],
            "titles": sorted titles}}
```

`gate`'s `before` and `after` are scores like `"3/4"`: `before` counts the baseline,
`after` counts the outcomes.

---

## Predict-then-run

Save a baseline from your week 7 cases against a real provider. Now make one
description in `kit.py` worse on purpose — shorten `find_notes` to *"Finds things."*
— and run again.

Predict which case regresses. Then run the gate and see whether the score alone would
have told you.

---

## Before you close the laptop

Commit, push, fill in the signal log. Read the milestone tonight.
