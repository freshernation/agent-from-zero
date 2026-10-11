# Day 3 — Dictionaries, and a conversation

> **By the end of today** you can describe one thing with a dictionary, and hold an
> entire conversation in a list of them.

---

## Read first

- [ ] [Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) — 15 min
- [ ] [Looping techniques](https://docs.python.org/3/tutorial/datastructures.html#looping-techniques) — first two examples · 5 min

---

## What you need to know

### A dictionary is labelled values

A list answers *"what is third?"*. A dictionary answers *"what is the title?"*.

```python
message = {"role": "user", "content": "Remember to buy milk"}

message["role"]              # "user"
message["content"]           # "Remember to buy milk"
message["when"] = "today"    # add a new key
"role" in message            # True
```

### The key that is not there

```python
message["author"]            # KeyError: 'author'     <- crashes
message.get("author")        # None                   <- does not
```

Use `[]` when the key **must** be there and its absence is a bug. Use `.get()` when it
is genuinely optional.

### A list of dictionaries

```python
history = [
    {"role": "user", "content": "Remember to buy milk"},
    {"role": "assistant", "content": "Saved."},
    {"role": "user", "content": "What did I ask?"},
]

for message in history:
    print(message["role"], "said", message["content"])
```

This is the single most important shape in the course. `role` says who is speaking.
`content` says what they said. A conversation with a model is this list, getting
longer.

### Counting with a dictionary

```python
counts = {}
for message in history:
    role = message["role"]
    if role not in counts:
        counts[role] = 0
    counts[role] = counts[role] + 1
# {"user": 2, "assistant": 1}
```

### Joining lines

```python
"\n".join(["one", "two"])     # "one\ntwo"  - a single string with a line break in it
```

---

## Exercises

```bash
pytest week-02/day-3 -v
```

All in `messages.py`.

| Function | Returns |
|---|---|
| `make_message(role, content)` | `{"role": role, "content": content}` |
| `add_message(history, role, content)` | appends a message **to that list** and returns how long the list now is |
| `count_by_role(history)` | `{"user": 2, "assistant": 1}`; `{}` for an empty history |
| `last_from(history, role)` | the `content` of the most recent message with that role, or `None` |
| `transcript(history)` | `"user: hi\nassistant: hello"`; `""` for an empty history |

`add_message` is the one function this week that is **meant** to change its input:
that is its whole job, and the name says so.

---

## Predict-then-run

```python
note = {"title": "milk"}
print(note["Title"])
```

Then the same with `.get("Title")`. One crashes and one silently gives you `None`.
Which would you rather have in a program you are debugging at 2am? There is a real
argument for each.

---

## Before you close the laptop

Commit, push, fill in the signal log.
