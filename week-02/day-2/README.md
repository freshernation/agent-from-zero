# Day 2 — Lists and `for`

> **By the end of today** you can keep many values in one list, visit each of them, and
> build a new list from an old one.

---

## Read first

- [ ] [Lists](https://docs.python.org/3/tutorial/introduction.html#lists) — 15 min
- [ ] [`for` statements](https://docs.python.org/3/tutorial/controlflow.html#for-statements) and [`range()`](https://docs.python.org/3/tutorial/controlflow.html#the-range-function) — 15 min

---

## What you need to know

### A list is values in order

```python
lines = ["hello", "/help", "bye"]
lines[0]            # "hello"    <- counting starts at 0
lines[-1]           # "bye"      <- -1 is the last one
len(lines)          # 3
lines.append("ok")  # now there are 4; append changes the list itself
"bye" in lines      # True
```

### `for` visits each one

```python
for line in lines:
    print(line)
```

Unlike `while`, a `for` loop cannot run forever — it stops when the list runs out.
Use `for` when you have the things; use `while` when you are waiting for a condition.

### The pattern you will write a hundred times

Start with an empty result, visit each item, add to the result, return it.

```python
def lengths(words):
    result = []
    for word in words:
        result.append(len(word))
    return result
```

The `return` is **outside** the loop. Indent it one level too far and the function
returns after the first item. That is Thursday's bug number three.

### Counting while you loop

```python
for number, line in enumerate(lines, start=1):
    print(number, line)         # 1 hello / 2 /help / 3 bye
```

### Do not change what you were handed

```python
def with_extra(items):
    items.append("extra")       # changes the CALLER'S list. They did not ask for that.
    return items
```

Build a new list instead. A function that quietly edits its input is the hardest kind
of bug to find.

---

## Exercises

```bash
pytest week-02/day-2 -v
```

All in `lists.py`.

| Function | Returns |
|---|---|
| `total(numbers)` | the sum; `0` for an empty list. Write the loop — no `sum()` today |
| `longest(words)` | the longest word; the first one on a tie; `""` for an empty list |
| `numbered(lines)` | `["1. hello", "2. bye"]` |
| `only_commands(lines)` | a **new** list of just the lines starting with `/` |

None of them may change the list they were given.

---

## Predict-then-run

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)
```

Two names, one list. This is the most surprising thing in beginner Python and it is
tomorrow's debugging exercise. Sit with it today.

---

## Before you close the laptop

Commit, push, fill in the signal log.
