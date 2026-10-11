# Day 3 — Pieces, and proving they work

> **By the end of today** you can split a program across files, and write the tests
> yourself instead of being handed them.

---

## Read first

- [ ] [Modules](https://docs.python.org/3/tutorial/modules.html) — sections 6.1 and 6.1.1 · 15 min
- [ ] [pytest: get started](https://docs.pytest.org/en/stable/getting-started.html) — the first two sections · 10 min

---

## What you need to know

### Your own files are modules

If `mathtools.py` sits next to `report.py`:

```python
# report.py
from mathtools import percent

print(percent(1, 4))
```

No folder names, no `.py`. The file name is the module name.

### Importing runs the file

`import mathtools` runs every line of `mathtools.py`, top to bottom. `def` lines just
define things, which is harmless. But an `input()` or a `print()` sitting at the top
level of the file runs too — at import time, in someone else's program.

### The guard

```python
def main():
    print(progress(3, 12))

if __name__ == "__main__":
    main()
```

`__name__` is `"__main__"` only when the file is the one being **run**. When it is
being **imported**, the block is skipped. Every file from now on is either all `def`s,
or `def`s plus this guard at the bottom.

### A test is a function that asserts

```python
# test_mine.py
import pytest
from mathtools import clamp

def test_clamp_leaves_a_value_in_range_alone():
    assert clamp(5, 0, 10) == 5

def test_percent_refuses_zero():
    with pytest.raises(ValueError):
        percent(1, 0)
```

`assert` says *"this must be true"*. pytest finds every function whose name starts with
`test_` in every file whose name starts with `test_`, runs it, and reports which
assertions failed.

### What makes a test good

A test is good if it **fails when the code is wrong**. That is the only measure. A test
that passes against broken code is decoration.

So for every function ask: what are the edges? Below the range, above it, exactly on
it. Zero. Empty. Today your tests are graded by running them against four deliberately
broken versions of `mathtools.py` — a good suite catches all four.

---

## Exercises

```bash
pytest week-03/day-3 -v
```

### 1. `mathtools.py`

| Function | Returns |
|---|---|
| `clamp(value, low, high)` | `value`, but no lower than `low` and no higher than `high` |
| `percent(part, whole)` | `part` as a percentage of `whole` — `percent(1, 4)` is `25.0`. Raises `ValueError("Cannot take a percentage of zero")` when `whole` is 0 |

### 2. `report.py`

Import from `mathtools`. Do not copy the functions across.

| Function | Returns |
|---|---|
| `progress(done, total)` | `"3 of 12 (25%)"` — the percentage rounded to a whole number and never above 100. When `total` is 0: `"nothing to do"` |
| `main()` | prints `progress(3, 12)` |

Put the call to `main()` behind the guard, so importing `report` prints nothing.

### 3. `test_mine.py`

Write at least **five** tests for `clamp` and `percent`. They must pass against your
`mathtools.py` and fail against each of four broken versions you cannot see.

---

## Predict-then-run

Put `print("loading mathtools")` at the top of `mathtools.py`, then run
`python3 report.py`. Then run `pytest week-03/day-3`. Count how many times it prints,
and work out why. Then delete the line.

---

## Before you close the laptop

Commit, push, fill in the signal log.
