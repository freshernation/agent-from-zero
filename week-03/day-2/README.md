# Day 2 — When it goes wrong

> **By the end of today** you can catch an error you expected, raise one on purpose,
> and write a tool that reports failure instead of crashing.

---

## Read first

- [ ] [Handling exceptions](https://docs.python.org/3/tutorial/errors.html#handling-exceptions) — 15 min
- [ ] [Raising exceptions](https://docs.python.org/3/tutorial/errors.html#raising-exceptions) — 5 min

---

## What you need to know

### Catching

```python
try:
    number = int(text)
except ValueError:
    number = None
```

Python tries the first block. If a `ValueError` happens inside it, Python jumps to the
`except` block instead of crashing. Any **other** error still crashes — which is what
you want, because an error you did not expect is a bug you need to see.

### Never do this

```python
try:
    number = int(txet)      # typo
except:                     # bare except: catches the NameError too
    number = None           # ...so the typo becomes "everything is None", silently
```

Always name the error.

### Raising

Your own functions can refuse:

```python
def percent(part, whole):
    if whole == 0:
        raise ValueError("Cannot take a percentage of zero")
    return part / whole * 100
```

`raise` stops the function immediately, like `return`, except the caller gets an error
instead of a value.

### Getting the message out

```python
try:
    percent(1, 0)
except ValueError as error:
    print(str(error))       # Cannot take a percentage of zero
```

### `eval`, and why it is dangerous

```python
eval("17 * 23")             # 391
```

`eval` runs a string as Python. All of Python. So this also works:

```python
eval("__import__('os').system('rm -rf ~')")
```

A calculator built on bare `eval` is a way to run any command on your machine. In
week 5 the string comes from a language model, which got it from a user, a web page or
a file. **Check every character first**, and only then evaluate.

Even the safe characters hide a trap: `9**9**9**9` is all digits and stars, and it
will freeze your computer working out a number with hundreds of millions of digits.

### The tool rule

A function meant for a model **never raises**. It returns a string either way:

```python
calculate_tool("17 * 23")     # "391"
calculate_tool("1 / 0")       # "Error: Cannot divide by zero"
```

---

## Exercises

```bash
pytest week-03/day-2 -v
```

### 1. `calc.py`

| Function | Does |
|---|---|
| `parse_int(text)` | the whole number in the text, or `None` if it is not one |
| `calculate(expression)` | the result as a number. **Raises** `ValueError`, with these exact messages: |
| | `Unsafe expression` — anything other than digits, spaces and `+ - * / ( ) .`, or any `**` |
| | `Cannot divide by zero` |
| | `Not a calculation` — safe characters that are not valid arithmetic, like `2 +` or `""` |
| `calculate_tool(expression)` | **never raises.** `"391"`, or `"Error: Unsafe expression"` |

Check the characters **before** you `eval`. Inside `calculate`, a `ZeroDivisionError`
and a `SyntaxError` each need turning into the right `ValueError`.

### 2. `storage.py`

| Function | Does |
|---|---|
| `load_or_empty(path)` | the data in that JSON file; `[]` if the file is missing **or** is not valid JSON |

The error `json.loads` raises on bad text is `json.JSONDecodeError`.

---

## Predict-then-run

```python
def risky():
    try:
        return int("abc")
    except ZeroDivisionError:
        return 0

print(risky())
```

Does the `except` help? Why not?

---

## Before you close the laptop

Commit, push, fill in the signal log.
