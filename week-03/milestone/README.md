# Week 3 Milestone — Project 1: Desk, with a memory

> Four files, each with one job. It remembers. It does not crash.

This is the first of the course's three projects, and the last program you write with
no model in it. In week 5 you hand these same functions to a model and delete the
command parser — the model becomes the parser.

---

## The files

| File | Job | Where it comes from |
|---|---|---|
| `notes.py` | add / list / find / delete | **Copy yours from `week-02/milestone/`**, unchanged |
| `calc.py` | the safe calculator | **Copy yours from `week-03/day-2/`**, unchanged |
| `store.py` | load and save | new |
| `app.py` | understand a typed command, and the loop | new |

If you have to change `notes.py` or `calc.py` to make this work, stop and ask why.
Code that needs editing every time it is reused was not finished.

---

## `store.py`

| Function | Does |
|---|---|
| `load_notes(path)` | the list of notes in that JSON file; `[]` if it is missing or damaged |
| `save_notes(path, notes)` | writes them as JSON |

## `app.py`

### `handle(notes, line)` → the reply, as a string

| The line | Reply |
|---|---|
| `add milk \| two litres` | whatever `add_note(notes, "milk", "two litres")` returns |
| `add milk` | the same with an empty body |
| `list` | `list_titles(notes)` |
| `find litres` | `find_notes(notes, "litres")` |
| `delete milk` | `delete_note(notes, "milk")` |
| `calc 17 * 23` | `calculate_tool("17 * 23")` |
| anything else, including an empty line | `Commands: add, list, find, delete, calc, quit` |

The command word may be in any capitals. Spaces around the title and body are removed.

`handle` does no printing, no saving and no `input()`. It turns a line into a reply —
which means you can test it without typing.

### `main()`

1. The file to use is the environment variable `NOTES_FILE`, or `notes.json` if that
   is not set: `os.environ.get("NOTES_FILE", "notes.json")`
2. Load the notes.
3. Loop: read a line with the prompt `> `. On `quit`, print `Bye.` and stop.
   Otherwise print the reply from `handle`, then save.

Call `main()` behind the `__name__` guard.

---

## Check it

```bash
pytest week-03/milestone -v
python3 week-03/milestone/app.py
```

Run it by hand. Add two notes, quit, run it again, and `list`. Then open `notes.json`
in your editor and look at what you made.

---

## Then make it good

- [ ] `app.py` contains no logic about notes — it only decides which function to call.
- [ ] Nothing outside `store.py` mentions JSON.
- [ ] There is no bare `except:` anywhere.
- [ ] You can say, for each file, the one reason it would ever need to change.

---

## Ship it

Commit and push. This is a portfolio piece: write three sentences at the top of
`app.py` saying what it is and how to run it.

## Friday

Rehearse with `ai/defend.md`, then the real defence.
