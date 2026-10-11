# Day 4 — Wrong without crashing

> **By the end of today** you can find a bug in a function that raises no error at all.

Last Thursday four of the five bugs came with a traceback. Today only one does. From
here on that is the normal ratio.

---

## What you need to know

### Put a `print` inside it

The fastest debugger ever invented:

```python
def count_user(history):
    count = 0
    for message in history:
        print("looking at", message)          # <- what is it actually seeing?
        if message["role"] == "User":
            count = count + 1
    return count
```

Print what the function is **actually** given and **actually** compares. The bug is
nearly always a gap between what you assumed was there and what is. Delete the prints
when you are done.

### Call it yourself, with something small

Do not debug through the tests. Open a scratch file, call the function with a
two-item list you can hold in your head, and print the result.

### The four silent bugs

| Symptom | Usual cause |
|---|---|
| Returns `None` | It `print`s instead of `return`ing, or a branch has no `return` |
| Returns after one item | `return` is indented inside the loop |
| The caller's list changed | Two names for one list — `copy = original` copies nothing |
| Always zero / always empty | A comparison that can never be true — capitals, a typo in a key |

---

## Exercises

```bash
pytest week-02/day-4 -v
```

Five files, one broken function each. The comment at the top says what it should do.
Fix each with the smallest change you can, and fill in `NOTES.md`.

For `broken_4.py`, to copy a list use `list(original)` — a new list with the same
items in it.

---

## Before you close the laptop

Commit, push, fill in the signal log.
