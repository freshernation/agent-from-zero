# Week 2 Milestone — The notes toolkit

> Four functions. In week 5 you will hand them to a model, unchanged.

A note is a dictionary: `{"title": "milk", "body": "two litres, semi-skimmed"}`.
All the notes are a list of those. Every function takes that list as its **first**
argument.

---

## What to build — `notes.py`

Every function returns **a sentence** — a string a person could read. Never a number,
never a list, never `None`. The reason arrives in week 5: the thing reading the answer
will be a model, and a model can only read text.

### `add_note(notes, title, body)`

Adds a note to the list.

| Situation | Returns | Adds? |
|---|---|---|
| normal | `Saved 'milk'.` | yes |
| the title is empty or only spaces | `A note needs a title.` | no |
| a note with that title exists (any capitals) | `There is already a note called 'milk'.` | no |

Store the title with the spaces around it removed.

### `list_titles(notes)`

```
1. milk
2. call the dentist
```

One per line, numbered from 1, in the order they were added. With no notes:
`No notes yet.`

### `find_notes(notes, word)`

Every note whose title **or** body contains the word, ignoring capitals — one per line,
as `title: body`:

```
milk: two litres, semi-skimmed
```

Nothing matches: `No notes mention 'cheese'.`

### `delete_note(notes, title)`

Removes the note with that title (any capitals) and returns `Deleted 'milk'.`
No such note: `No note called 'cheese'.`

To remove an item from a list: `notes.remove(note)`.

---

## Check it

```bash
pytest week-02/milestone -v
```

---

## Then make it good

- [ ] "Find the note with this title, ignoring capitals" appears in two functions.
      Write it **once**, as a fifth function, and call it from both.
- [ ] No function prints.
- [ ] Every sentence a function can return is written in the code exactly once.

---

## Friday

Rehearse with `ai/defend.md`, then the real defence with your instructor.
