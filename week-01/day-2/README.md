# Day 2 — Numbers and decisions

> **By the end of today** your program can do arithmetic on what a person types and
> take a different path depending on the answer.

---

## Read first

- [ ] [`if` statements](https://docs.python.org/3/tutorial/controlflow.html#if-statements) — 10 min
- [ ] [Numbers](https://docs.python.org/3/tutorial/introduction.html#numbers) — 15 min

---

## What you need to know

### `input()` gives you text. Always.

```python
count = input("Messages sent: ")     # the person types 3
print(count * 2)                     # 33   <- "3" twice, not six
```

Convert before you calculate:

```python
count = int(input("Messages sent: "))        # whole number
price = float(input("Price per message: "))  # number with a decimal point
print(count * price)
```

### Money has two decimal places

```python
total = 1.5
print(f"Total: ${total:.2f}")        # Total: $1.50
```

`:.2f` means *"show this as a number with exactly two decimals"*.

### Comparing

```python
3 == 3       # True     <- two equals signs ASK; one equals sign ASSIGNS
3 != 4       # True
"a" == "A"   # False    <- capitals matter
```

### Choosing

```python
if steps > limit:
    print("Over")
elif steps == limit:
    print("At the limit")
else:
    print("OK")
```

Python checks from the top and runs the **first** branch that is true, then skips the
rest. The indentation is not decoration — it is how Python knows what is inside the `if`.

### Tidying text before you compare it

```python
text = "  Hello  "
text.strip()            # "Hello"      <- spaces off both ends
text.strip().lower()    # "hello"
```

People type capitals and stray spaces. Compare the tidy version.

---

## Exercises

```bash
pytest week-01/day-2 -v
```

### 1. `cost.py`

Ask `Messages sent: ` then `Price per message: `. Print the total with two decimals:

```
Total: $1.50
```

(3 messages at 0.5 each.)

### 2. `limit.py`

Ask `Steps used: ` then `Step limit: `. Print exactly one of:

| When | Print |
|---|---|
| used is below the limit | `OK` |
| used equals the limit | `At the limit` |
| used is above the limit | `Over the limit by 2` (the real difference) |

You are writing a step limit. In week 6 the same three lines stop an agent that will
not stop itself.

### 3. `reply.py`

Ask `You: ` and print one line:

| The person typed | Print |
|---|---|
| `hello` | `Bot: Hi there!` |
| `bye` | `Bot: Goodbye!` |
| nothing at all | `Bot: Say something.` |
| anything else, e.g. `pizza` | `Bot: I don't understand "pizza".` |

`HELLO` and `  hello  ` count as `hello`. In the last row, echo back the tidy version.

---

## Predict-then-run

```python
answer = input("Number: ")     # you type 5
if answer == 5:
    print("five")
else:
    print("not five")
```

Which line prints, and why? Fix it two different ways.

---

## Before you close the laptop

Commit, push, fill in the signal log.
