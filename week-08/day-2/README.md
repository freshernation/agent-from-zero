# Day 2 — Tools first

> **By the end of today** every tool in your spec works, is tested, and has never been
> near a model.

This is weeks 2 and 3 again, and it is the day that decides whether Wednesday is
pleasant. An agent built on tools that mostly work is undebuggable: you can never tell
whether the model was wrong or the tool was.

---

## What to build — `project/tools.py`

| Name | What it is |
|---|---|
| your tool functions | at least four; plain arguments in, a sentence out, never raising on bad input |
| `EMPTY` | the empty state of your data — usually `[]` or `{}` |
| `reset(state)` | replace everything in the data file with `state` |
| `snapshot()` | return the whole current state |
| `SCHEMAS` | one schema per tool |
| `TOOLS` | the dispatch table |
| `DANGEROUS` | the set of tool names that need a human's yes. It may be empty — but then `SPEC.md` must say why |
| `run_tool(tools, name, args)` | runs one tool and returns a string, whatever happens: `Error: unknown tool 'xyz'` for a name that is not there, `Error: <ErrorName>: <message>` for anything that goes wrong. You wrote this in week 5 and `kit.py` has carried it since. There is no kit this week |

The data lives in the file named by `os.environ.get("DATA_FILE", "data.json")`.
Read that **inside** each function, not once at the top of the file — the tests point
it somewhere else for every test.

`reset` and `snapshot` are not tools. The model never sees them. They exist so that
tomorrow's evals can set up a starting state and check an ending one.

---

## Write your own tests first

Create `project/test_tools.py`. For each tool: the normal case, the empty case, and at
least one piece of nonsense. You wrote tests in week 3; this is why.

The contract tests only check the **shape** — that there are tools, that they return
sentences, that nonsense does not crash them. Whether `finish_book` really marks the
book finished is something only your own tests can know.

---

## Check it

```bash
pytest week-08/project/test_tools.py -v
pytest week-08/project -k Tools -v
```

---

## Before you close the laptop

Commit, push, fill in the signal log.
