# Day 1 — Functions

> **By the end of today** you can write a function that takes values in and hands a
> value back, and you will never again confuse `return` with `print`.

---

## Read first

- [ ] [Defining functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions) — 20 min
- [ ] [Default argument values](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values) — first half · 10 min

---

## What you need to know

### A function is a named action

```python
def shout(text):
    return text.upper() + "!"

shout("hello")          # "HELLO!"
loud = shout("stop")    # the result can be stored, compared, passed on
```

`text` is a **parameter** — a name for whatever gets handed in. It exists only inside
the function.

### `return` is not `print`

```python
def bad(text):
    print(text.upper())      # shows it to a human. Hands back nothing.

def good(text):
    return text.upper()      # hands it back. Shows nothing.

x = bad("hi")     # prints HI, and x is None
y = good("hi")    # prints nothing, and y is "HI"
```

`print` is for people. `return` is for the rest of the program. Every tool you ever
give an agent must `return`, because the thing reading the answer is not a person
looking at a screen.

### A function stops at `return`

```python
def sign(n):
    if n < 0:
        return "negative"
    return "not negative"     # only reached if the first return did not happen
```

### Default values

```python
def greeting(name, excited=False):
    if excited:
        return f"Hello, {name}!"
    return f"Hello, {name}."

greeting("Sam")                  # "Hello, Sam."
greeting("Sam", excited=True)    # "Hello, Sam!"
```

### Two string tools you will use all course

```python
"one two  three".split()         # ["one", "two", "three"]   <- a list; more tomorrow
len("one two  three".split())    # 3
"/help".startswith("/")          # True
```

---

## Exercises

```bash
pytest week-02/day-1 -v
```

All four go in `text_tools.py`.

| Function | Returns |
|---|---|
| `shout(text)` | the text in capitals with `!` on the end |
| `word_count(text)` | how many words — `""` is 0, and extra spaces do not count |
| `is_command(text)` | `True` if the text, ignoring spaces around it, starts with `/` |
| `greeting(name, excited=False)` | `"Hello, Sam."` or, when excited, `"Hello, Sam!"` |

`word_count` is the first function you write that an agent will call later. Keep it.

---

## Predict-then-run

```python
def add(a, b):
    print(a + b)

total = add(2, 3) + 1
```

What happens? Not "what is `total`" — what *happens*? Read the last line of the error.

---

## Before you close the laptop

Commit, push, fill in the signal log.
