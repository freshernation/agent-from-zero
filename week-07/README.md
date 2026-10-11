# Week 7 — Trust it

> **Destination**
> Decide what your agent is allowed to do without asking, make it remember the right
> things, and prove — with numbers — that it works.

Last week the question was *"can I make it work?"* This week it is *"should I let it?"*
The code is easier than week 6. The judgement is harder.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Put a human between the model and anything it cannot undo |
| Tue | `day-2/` | Carry a conversation across tasks, cut it safely, and give the agent a long-term memory |
| Wed | `day-3/` | Write evals: tasks with checkable outcomes, and a score |
| Thu | `day-4/` | Give a run a budget, and retry a model that is briefly unavailable |
| Fri | `milestone/` | Ship a Desk you would actually let near your own files, with the eval report to back it |

---

## The four questions

Every agent that touches something real has to answer these. One per day.

1. **What can it break?** — and who has to say yes first.
2. **What does it know?** — and what happens when that gets too long.
3. **How do you know it works?** — not "it worked when I tried it".
4. **What does it cost when it goes wrong?** — in money, and in retries.

---

## Your agent keeps growing

Monday starts from your week 6 `agent.py`. Each day you copy the previous day's file
and add to it. By Friday `run_agent` takes more than a dozen arguments, and that is a
real signal: it is the point at which professional code reaches for a configuration
object. You have not met classes, so you will feel the pain instead — which is the
best possible preparation for understanding why they exist.

---

## Outside-view question

> *How does a bank decide which transactions a cashier can approve alone and which
> need a manager, and where would you draw that line for an agent?*
