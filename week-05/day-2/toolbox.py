"""The five things Desk can do - given to you, complete.

This is weeks 2 and 3 again: the notes functions and the safe calculator, with
the notes kept in a JSON file. Nothing in here knows a model exists. These are
ordinary Python functions, and that is the point - a "tool" is just a function
you are willing to let a model ask for.

Every function takes plain arguments and returns a SENTENCE, even when it fails.

The notes live in the file named by the NOTES_FILE environment variable, or
notes.json in the current folder if that is not set.
"""

import json
import os
from pathlib import Path

SAFE_CHARACTERS = "0123456789+-*/(). "


def _path():
    return Path(os.environ.get("NOTES_FILE", "notes.json"))


def _load():
    path = _path()
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return []


def _save(notes):
    _path().write_text(json.dumps(notes, indent=2))


def _find(notes, title):
    wanted = title.strip().lower()
    for note in notes:
        if note["title"].lower() == wanted:
            return note
    return None


def add_note(title, body=""):
    notes = _load()
    title = title.strip()
    if title == "":
        return "A note needs a title."
    existing = _find(notes, title)
    if existing is not None:
        return f"There is already a note called '{existing['title']}'."
    notes.append({"title": title, "body": body})
    _save(notes)
    return f"Saved '{title}'."


def list_titles():
    notes = _load()
    if not notes:
        return "No notes yet."
    lines = []
    for number, note in enumerate(notes, start=1):
        lines.append(f"{number}. {note['title']}")
    return "\n".join(lines)


def find_notes(word):
    wanted = word.lower()
    lines = []
    for note in _load():
        if wanted in note["title"].lower() or wanted in note["body"].lower():
            lines.append(f"{note['title']}: {note['body']}")
    if not lines:
        return f"No notes mention '{word}'."
    return "\n".join(lines)


def delete_note(title):
    notes = _load()
    note = _find(notes, title)
    if note is None:
        return f"No note called '{title}'."
    notes.remove(note)
    _save(notes)
    return f"Deleted '{note['title']}'."


def calculate(expression):
    for character in expression:
        if character not in SAFE_CHARACTERS:
            return "Error: Unsafe expression"
    if "**" in expression:
        return "Error: Unsafe expression"
    try:
        return str(eval(expression))
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except (SyntaxError, TypeError):
        return "Error: Not a calculation"
