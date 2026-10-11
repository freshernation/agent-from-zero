# Day 1 — Make it remember

> **By the end of today** your data survives the program ending.

---

## Read first

- [ ] [Reading and writing files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files) — 15 min
- [ ] [Saving structured data with `json`](https://docs.python.org/3/tutorial/inputoutput.html#saving-structured-data-with-json) — 10 min
- [ ] [Modules](https://docs.python.org/3/tutorial/modules.html) — the first screen only · 5 min

---

## What you need to know

### `import`

Python ships with a library of ready-made modules. You ask for one by name:

```python
import json
from pathlib import Path
```

### JSON is data written down as text

```python
notes = [{"title": "milk", "body": "two litres"}]

text = json.dumps(notes, indent=2)      # Python data  ->  a string
back = json.loads(text)                 # a string     ->  Python data
back == notes                           # True
```

`dumps` and `loads` end in **s** for *string*. JSON looks almost exactly like Python
lists and dictionaries, on purpose. It is also the language every web API speaks —
including every model API. When a model "calls a tool", what it actually produces is
JSON.

Three differences worth knowing: JSON uses `true` / `false` / `null`, always double
quotes, and no trailing commas.

### Files

```python
path = Path("notes.json")

path.write_text(text)        # create or REPLACE the file
text = path.read_text()      # the whole file as one string
path.exists()                # True / False
```

`write_text` replaces everything that was there. There is no undo.

### Save and load are a pair

```python
def save(path, data):
    Path(path).write_text(json.dumps(data, indent=2))
```

Loading is the reverse — and it has to decide what to do the first time the program
ever runs, when there is no file yet.

---

## Exercises

```bash
pytest week-03/day-1 -v
```

All in `storage.py`.

| Function | Does |
|---|---|
| `to_json(data)` | returns the data as a JSON string, indented by 2 |
| `from_json(text)` | returns the Python data in a JSON string |
| `save(path, data)` | writes the data to that file as JSON; returns nothing |
| `load(path)` | returns the data in that file — or `[]` if the file does not exist |

`path` arrives as a string or a `Path`; `Path(path)` handles both.

---

## Predict-then-run

```python
import json
print(json.dumps({"done": True, "owner": None, "n": 3}))
print(json.loads('{"title": "milk"}')["title"])
print(json.loads("{'title': 'milk'}"))
```

The third line fails. Read the error and say what JSON wanted.

---

## Before you close the laptop

Commit, push, fill in the signal log.
