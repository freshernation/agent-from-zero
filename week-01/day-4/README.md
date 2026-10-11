# Day 4 — Read the error

> **By the end of today** you can read a traceback from the bottom up, find the line,
> and fix code you did not write.

No new Python today. Debugging is half the job, and it is the half nobody teaches.

---

## Read first

- [ ] [Errors and exceptions](https://docs.python.org/3/tutorial/errors.html) — sections 8.1 and 8.2 only · 10 min

---

## What you need to know

### A traceback is read from the bottom

```
Traceback (most recent call last):
  File "broken.py", line 2, in <module>
    print(f"You sent {message_count} messages.")
NameError: name 'message_count' is not defined
```

1. **Last line** — what went wrong, in Python's words.
2. **The line above it** — where. File name and line number.
3. Only then look at your code.

### The four you will meet most

| Error | Plain English |
|---|---|
| `SyntaxError` | Python could not even read the file. Look at that line *and the one before*. |
| `NameError` | You used a name that does not exist. Usually a typo. |
| `TypeError` | You combined two things that do not combine — text and a number, say. |
| `ValueError` | Right kind of thing, impossible value — `int("hello")`. |

### The two with no error at all

- **The loop that never ends.** Nothing is printed, or the same thing forever. Ask:
  what makes it stop, and does that ever change?
- **The wrong answer.** The program runs and is simply incorrect. Nothing will tell you.
  You find these by predicting the output first and noticing it is different.

That last kind is the dangerous one. Every agent bug you meet in week 6 is of that kind.

### The method

1. **Reproduce it.** Run it. See it fail yourself.
2. **Read** the last line of the traceback, then the line number.
3. **Predict** what the line should do. Compare with what it does.
4. **Change one thing.** Run again.

---

## Exercises

```bash
pytest week-01/day-4 -v
```

Five broken files. Each has a comment at the top saying what it *should* do. Fix each
with the smallest change you can — usually a single line — and fill in `NOTES.md` as
you go. The notes are what Friday's defence is about.

`broken_4.py` will not stop on its own. <kbd>Ctrl</kbd>+<kbd>C</kbd>.

---

## Before you close the laptop

Commit, push, fill in the signal log.
