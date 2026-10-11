# Day 3 — Go round again

> **By the end of today** your program can repeat something until a condition says stop
> — and you can say what that condition is.

A loop is the most powerful thing you have met and the easiest to get wrong. The
question to ask of every loop, forever: **what makes it stop?**

---

## Read first

- [ ] [`while` in the tutorial's first steps](https://docs.python.org/3/tutorial/introduction.html#first-steps-towards-programming) — 15 min
- [ ] [`break`](https://docs.python.org/3/tutorial/controlflow.html#break-and-continue-statements) — 10 min

---

## What you need to know

### `while`

```python
count = 3
while count > 0:
    print(count)
    count = count - 1
print("done")
```

Python checks the condition. If it is true, it runs the indented block, then **goes
back and checks again**. When the condition is false, it carries on underneath.

Delete the `count = count - 1` line and the condition never becomes false. That is an
infinite loop. Press <kbd>Ctrl</kbd>+<kbd>C</kbd> to stop one.

### `while True` and `break`

When the stopping condition is only known in the middle of the block:

```python
while True:
    text = input("You: ")
    if text == "quit":
        break                # leave the loop right now
    print(f"Bot: {text}")
print("Bot: Bye!")
```

Read that one carefully. **Read a line, decide, respond, go round.** It is the shape of
every chat program and every agent you will ever write.

### Counting as you go

```python
turns = 0
while turns < 5:
    turns = turns + 1
print(turns)        # 5
```

### Two ways out

Real loops usually have two exits: the job is finished, or a limit was hit. The limit
is the one people forget, and it is the one that saves you.

---

## Exercises

```bash
pytest week-01/day-3 -v
```

### 1. `countdown.py`

Ask `Start: `. Count down from that number to 1, one per line, then print `Liftoff!`.
A start of `0` prints only `Liftoff!`.

### 2. `echo.py`

Loop: ask `You: `, print `Bot: ` followed by what was typed. When the person types
`quit` (any capitals), print `Bot: Bye!` and stop — without echoing `quit`.

### 3. `budget.py`

Ask `Budget: ` once. Then keep asking `Cost: ` and subtracting it. As soon as the
budget reaches zero or below, print how many costs were entered and stop:

```
Out of budget after 3 steps.
```

(Budget `10`, costs `4`, `4`, `4`.) Nobody typed `quit` there. The loop stopped itself
because a number ran out — which is exactly how you will stop an agent from spending
money forever.

---

## Predict-then-run

```python
n = 10
while n != 0:
    n = n - 3
print("finished")
```

Does it finish? Trace `n` on paper for five rounds before you run it. Then change one
character so that it does.

---

## Before you close the laptop

Commit, push, fill in the signal log.
