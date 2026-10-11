# Week 7 Milestone — A Desk you would trust

> The same agent, now gated, remembering, budgeted — and measured.

---

## The files

| File | Where it comes from |
|---|---|
| `kit.py` | given |
| `guards.py`, `agent.py`, `retry.py` | **copy from day 4** |
| `gate.py` | **copy from day 1** |
| `memory.py` | **copy from day 2** |
| `evals.py` | **copy from day 3** |
| `desk.py` | new |
| `cases.py` | new — your eval suite |
| `run_evals.py` | given |
| `EVAL_REPORT.md` | new — your results |

## `desk.py`

| Name | What it is |
|---|---|
| `SYSTEM` | your system prompt, 40 words or more. It now has to cover memory (when to `remember`, when to `recall`) and what to do when an action is refused |
| `DANGEROUS` | the set of tool names that need approval. At least `delete_note` |
| `TOKEN_BUDGET` | a number: the most tokens one turn may use |
| `ALL_SCHEMAS` | the kit's schemas followed by the memory schemas |
| `ALL_TOOLS` | one dispatch table holding the kit's tools and the memory tools |
| `take_turn(model, history, task, approve=None, wait=time.sleep)` | runs the agent once, continuing `history`, with everything above switched on. Returns `{"text": ..., "history": ...}` |
| `main()` | `connect()`; loop on `You: `; approvals asked in the terminal; print `Desk: <text>`; `quit` → `Bye.` |

`take_turn` returns:

- `"text"` — the answer, then on a second line how it ended: `(done, 2 steps)`
- `"history"` — what to pass as `history` next time: `carry(history, result)`

---

## `cases.py`

`CASES` — a list of at least **six** eval cases of your own, in Wednesday's format.
Between them they must include:

- a case with starting `notes`,
- a case that checks `titles`,
- a case that uses `never_calls`,
- a case where the starting titles and the expected titles are **the same** — a task
  after which nothing should have changed.

A case may also carry `"user_approves": True`, meaning the person at the keyboard
would have said yes to a dangerous action. Without it, `run_evals.py` refuses.

Write the cases you are afraid of.

## `EVAL_REPORT.md`

Run your suite against a **real** model:

```bash
python3 week-07/milestone/run_evals.py
```

Paste the output into `EVAL_REPORT.md` and answer the questions there. If a case
fails, decide which is wrong: the agent, the prompt, a tool description, or the case.
Fix it, run again, and record **both** runs. A report that shows 4/6 becoming 6/6,
with the reason, is worth more than one that only shows 6/6.

---

## Check it

```bash
pytest week-07/milestone -v
python3 week-07/milestone/desk.py
```

---

## Friday

Rehearse with `ai/defend.md`, then the real defence. Bring the eval report.
