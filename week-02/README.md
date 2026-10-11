# Week 2 — Names for actions, rows of things

> **Destination**
> Write functions that take values and return values, and hold a whole conversation in
> a list of dictionaries.

Last week's programs ran top to bottom and talked to a person. This week's are made of
**functions** — small named actions that something else calls. That "something else"
is the tests today. In week 5 it is a language model.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Write a function, and know the difference between `return` and `print` |
| Tue | `day-2/` | Keep many values in a list and visit each one |
| Wed | `day-3/` | Describe a thing with a dictionary, and a conversation with a list of them |
| Thu | `day-4/` | Debug functions that are wrong without crashing |
| Fri | `milestone/` | Ship the notes toolkit — four functions an agent will call in week 5 |

---

## The one idea to leave with

By Wednesday you will have written this:

```python
history = [
    {"role": "user", "content": "Remember to buy milk"},
    {"role": "assistant", "content": "Saved."},
]
```

That is not a simplified teaching version of how chat models are driven. That **is**
how they are driven. Every model API on earth takes a list that looks like this.

---

## Tests work differently from now on

Last week the tests ran your file and read what it printed. From now on they **import
your file and call your functions**. So:

- A function that `print`s its answer instead of `return`ing it fails every test.
- Code at the top level of the file (an `input()`, a stray `print`) runs when the test
  imports it. Keep the file to `def`s.

---

## Outside-view question

> *How does a kitchen brigade split work between stations, and what does that say
> about when a function should be two functions?*

---

## Milestone

A notes toolkit: add, list, find, delete. Every function returns a **sentence**, not a
number or a list — because in three weeks the thing reading the return value will be a
model, and models read sentences.
