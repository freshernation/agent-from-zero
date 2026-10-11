# Week 2 — Concept fence

## Allowed

**Everything from Week 1**, plus:

- `def`, parameters, `return`, default values (`def f(x, loud=False)`)
- `None`, and the fact that a function with no `return` gives you `None`
- Lists: `[]`, indexing, `len()`, `.append()`, `in`, `+` to join two lists
- `for item in items:` and `range()`, `enumerate()`
- String methods: `.split()`, `.join()`, `.upper()`, `.startswith()`, `in` for substrings
- Dictionaries: `{}`, `d["key"]`, `d.get("key")`, `"key" in d`, adding a key
- A list of dictionaries, and looping over one

## Not yet

`import` and any library · `try` / `except` · files · JSON · classes ·
comprehensions · `lambda` · sets and tuples · slicing beyond `items[0]` and
`items[-1]` · any model, API or agent

---

## Why the fence exists

A list comprehension is one line and a `for` loop is three. This week the three-line
version is the right answer, because you can put a `print` in the middle of it and
watch it work. You cannot debug what you cannot see inside.
