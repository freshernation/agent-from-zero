# Day 1 — Make the machine do something

> **By the end of today** you can write a file, run it, store a value under a name, and
> print exactly what you meant.

Today's real lesson is not `print()`. It is this: **the computer does exactly what you
say, and nothing else.** Every bug you hit for the rest of your life is a version of
that sentence.

---

## Read first

- [ ] [An informal introduction to Python](https://docs.python.org/3/tutorial/introduction.html) — sections 3.1.1 and 3.1.2 only · 25 min
- [ ] [f-strings](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals) — 10 min

---

## What you need to know

### Running a file

Make a file ending in `.py`. Put code in it. Run it:

```bash
python3 hello.py
```

Edit, save, run, look. You will do it ten thousand times.

### `print()`

```python
print("Hello")        # Hello
print("a", "b")       # a b      <- print puts a space between values
print(3 + 4)          # 7        <- no quotes: a calculation
print("3 + 4")        # 3 + 4    <- quotes: just text
```

The difference between those last two lines is the difference between a number and a
picture of a number. It comes back all week.

### Variables

A variable is a name stuck on a value.

```python
name = "Ada"
turns = 3
turns = turns + 1      # read the right side first: 3 + 1, then re-stick the name
print(name, turns)     # Ada 4
```

`=` does not mean "equals". It means **"make this name point at that value"**.

### f-strings

Put an `f` before the quote and Python fills in anything inside `{}`:

```python
print(f"{name} has spoken {turns} times.")     # Ada has spoken 4 times.
```

### `input()`

```python
name = input("What is your name? ")
```

The program stops, waits for a line, and hands it to you **as text** — always text,
even if the person typed `42`. Tomorrow that matters.

### `len()`

```python
len("Ada")      # 3
```

---

## Exercises

Do them in order. Run the tests after each one.

```bash
pytest week-01/day-1 -v
```

### 1. `hello.py`

Print exactly three lines:

1. `Hello, world!` — exactly that
2. Your name
3. One line on why you are doing this course

Line 1 is checked exactly. Write something true on line 3; you will read it again in
week 9 when it is hard.

### 2. `card.py`

The file starts with three variables. **Leave those three lines exactly as they are**
and print, underneath them, this line built from the variables:

```
Ada (tutor) has spoken 3 times.
```

The tests swap in different values, so typing the sentence out by hand will fail.

### 3. `greet.py`

Ask `What is your name? ` (with that exact prompt, including the space), then print two
lines:

```
Hello, Sam!
Your name has 3 letters.
```

---

## Before you close the laptop

```bash
git add -A
git commit -m "week 1 day 1"
git push
```

Then fill in `logs/signal-log.md`. Two minutes.

---

## Predict-then-run

Write your prediction down, then run it.

```python
print("2" + "2")
print(2 + 2)
print("2" * 3)
```

If any of those surprised you, that surprise is the most valuable thing that happened
today. Bring it to the live hour.
