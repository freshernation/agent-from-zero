# Day 3 — Wire it, then measure it

> **By the end of today** your agent runs against a real model and you have a number
> for how well.

---

## 1. Bring your loop

Copy from `week-07/milestone/` into `project/`:

```
agent.py   guards.py   gate.py   memory.py   retry.py   evals.py
```

`guards.py`, `gate.py`, `retry.py` and `memory.py` need **no changes at all**.

`agent.py` needs exactly **one line** changed. It begins `from kit import run_tool`,
and there is no kit here — `kit.py` was the notes. Import `run_tool` from your own
`tools.py` instead.

That is the whole port. If your loop needs anything else edited to run a completely
different set of tools, it had notes baked into it somewhere — find where, and ask
why.

## 2. `project/app.py`

| Name | What it is |
|---|---|
| `SYSTEM` | your system prompt, 40 words or more |
| `take_turn(model, history, task, approve=None, wait=time.sleep)` | exactly as in week 7, with your `SCHEMAS`, `TOOLS` and `DANGEROUS`. Returns `{"text", "history"}` |
| `main()` | the terminal loop |

## 3. Generalise the evals

Week 7's `evals.py` knows about notes: it writes a notes file and reads titles. Yours
must know about **your** data instead. Two small changes:

- `run_case` calls `reset(case.get("state", EMPTY))` before the run and `snapshot()`
  after it, in place of the notes file.
- `check(result, expect, state)` takes the snapshot, and the `titles` check becomes a
  `state` check. Its failure sentence is `state: expected <expected>, got <actual>`.

Everything else — `stopped`, `calls`, `never_calls`, `max_steps`, `answer_contains`,
`report` — stays as it is.

## 4. `project/cases.py`

`CASES`: at least **eight**. Include, as a minimum:

- two plain happy paths,
- one request that needs **three or more** steps,
- one **impossible** request, expecting the state unchanged,
- one case with `never_calls`,
- one **injected instruction** in the starting state, expecting the state unchanged,
- one for each dangerous tool, without approval, expecting the state unchanged.

## 5. Run it

`project/run_evals.py` is given.

```bash
python3 week-08/project/run_evals.py
```

Paste the first run into `project/EVAL_REPORT.md` **before you fix anything**.

---

## Check it

```bash
pytest week-08/project -k "Agent or Evals" -v
```

---

## Before you close the laptop

Commit, push, fill in the signal log.
