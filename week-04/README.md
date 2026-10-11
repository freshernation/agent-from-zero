# Week 4 — Talking to a model

> **Destination**
> Drive a language model from code — with either provider — and explain what every
> part of the request and the reply is for.

A model call is a function call that goes over the internet. You send a **list of
messages** (Wednesday of week 2) as **JSON** (Monday of week 3), and you get JSON back.
It can fail (Tuesday of week 3). You already own every piece.

From this week the AI may write code with you, and the rule that replaces "AI-off" is:
**you may not commit a line you could not have written and cannot explain on Friday.**

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Make a call, steer it with a system prompt, and read the reply |
| Tue | `day-2/` | Hold a conversation with something that has no memory |
| Wed | `day-3/` | Count the cost, notice a cut-off, and get JSON you can trust |
| Thu | `day-4/` | Open the box: the same request in Claude's dialect and OpenAI's |
| Fri | `milestone/` | Ship a chat assistant with memory and a cost meter, on any provider |

---

## Everything takes a `model`

```python
from llm import connect

model = connect()                                   # whichever provider .env names
reply = model.chat([{"role": "user", "content": "Hello"}])
```

`reply` is a dictionary:

| Key | Holds |
|---|---|
| `reply["text"]` | what the model said |
| `reply["stop"]` | why it stopped: `"done"`, `"length"`, `"refused"` — and next week, `"tools"` |
| `reply["usage"]` | `{"input": 12, "output": 5}` — tokens, which is what you pay for |
| `reply["message"]` | the assistant's turn as a message, ready to append to your list |
| `reply["tool_calls"]` | empty until next week |

Every function you write takes `model` as its **first argument** instead of calling
`connect()` itself. The tests pass in a `FakeModel` — scripted, free, instant, and
identical every run. Your code cannot tell the difference, which is the entire point.

```python
from llm import FakeModel, say

model = FakeModel([say("Hello there")])     # will reply with exactly that
model.requests[0]["messages"]               # afterwards: exactly what you sent
```

---

## Three providers, one setting

| `AGENT_PROVIDER` | What it is | Needs |
|---|---|---|
| `fake` (default) | repeats your message back | nothing |
| `claude` | Anthropic's Claude | `ANTHROPIC_API_KEY` |
| `openai` | OpenAI's models | `OPENAI_API_KEY` |

Set it in `.env` (see `SETUP.md`, "Before week 4"). Run `python3 week-04/try_it.py`
once with a real key, so the fake never feels like the whole story. A week of this
course costs well under a dollar on either provider.

---

## The four things that will surprise you

**It is not a function.** The same input gives different output. Anything you build on
top has to survive that.

**It will not follow your format.** Ask for JSON and sometimes you get JSON wrapped in
a friendly sentence. Handling that is not a hack — it is the job.

**It has no memory.** Every call is the first one. A conversation is you resending the
whole history, every time.

**It charges by the token, in both directions.** You pay for what you send *and* what
comes back — including, on some models, thinking you never see.

---

## Outside-view question

> *How does a translator at the UN handle a speaker who rambles, and what does that
> tell you about writing a system prompt?*
