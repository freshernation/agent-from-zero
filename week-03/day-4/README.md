# Day 4 — Files, JSON, and errors that hide

> **By the end of today** you can debug the three things that go wrong at the edge of a
> program: a file, a format, and an `except` that caught too much or too little.

---

## What you need to know

### Look at the file

When saving or loading misbehaves, stop reading code and **open the file**. Is it
there? Is it empty? Is it JSON, or something that only looks like it?

```
[{'title': 'milk'}]      <- Python's way of printing a list. Single quotes. Not JSON.
[{"title": "milk"}]      <- JSON.
```

### A path is not its contents

```python
json.loads("notes.json")       # tries to parse the nine characters n-o-t-e-s-...
json.loads(Path("notes.json").read_text())      # parses what is IN the file
```

### An `except` can be wrong in two directions

| Too wide | Too narrow |
|---|---|
| `except:` catches everything, including your typos | `except ZeroDivisionError:` when the thing that actually happens is a `ValueError` |
| Symptom: no crash, wrong answer, every time | Symptom: a crash you thought you had handled |

To find out which error **really** happens, delete the `try` for a moment and read the
traceback. Then put it back with the right name.

---

## Exercises

```bash
pytest week-03/day-4 -v
```

Four files, one broken function each. Smallest change you can. Fill in `NOTES.md`.

---

## Before you close the laptop

Commit, push, fill in the signal log.
