# Week 3 — Concept fence

## Allowed

**Everything from Weeks 1–2**, plus:

- `import`, `from x import y`, and importing your own files
- `json.dumps`, `json.loads`, including `indent=`
- Reading and writing text files: `open()` with `with`, or `Path.read_text()` /
  `Path.write_text()`; `Path.exists()`
- `try` / `except SomeError`, `raise ValueError("message")`, `str(error)`
- `if __name__ == "__main__":`
- `os.environ.get("NAME", default)`
- `assert` and writing a `test_*.py` file for pytest
- Slicing a string: `text[4:]`; and `.split("|", 1)`

## Not yet

Classes · decorators · generators · comprehensions · `lambda` · `*args` / `**kwargs` ·
databases · `async` · any model, API or agent

---

## Two rules inside the fence

**Never write a bare `except:`.** Name the error you expect. A bare `except` catches
your typos too, and turns a bug you could have read into a wrong answer you cannot.

**Never `eval` what you have not checked.** Tuesday shows you why.
