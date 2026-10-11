# Day 4 — What does it cost when it goes wrong?

> **By the end of today** a run cannot spend more than you allow, and a model that is
> briefly unavailable does not end the run.

---

## Read first

- [ ] Claude — [Errors](https://platform.claude.com/docs/en/api/errors) and [Rate limits](https://platform.claude.com/docs/en/api/rate-limits) · 15 min
- [ ] OpenAI — [Rate limits](https://platform.openai.com/docs/guides/rate-limits) — "Retrying with exponential backoff" · 10 min

---

## What you need to know

### Two kinds of failure

| | Example | Will trying again help? |
|---|---|---|
| **Transient** | rate limit, server overloaded, network blip | Yes — in a moment |
| **Permanent** | wrong API key, malformed request | No. Never. |

`ModelError` tells you which: `error.retryable` is `True` or `False`. Retrying a
permanent failure three times is three times as slow and exactly as broken.

### Back off

If the provider says *"too many requests"*, asking again instantly makes it worse.
Wait, and wait **longer** each time:

```python
2 ** 0      # 1 second before the first retry
2 ** 1      # 2 before the second
2 ** 2      # 4 before the third
```

That is **exponential backoff**. Every production client does it.

### Sleeping is an argument

```python
def call_with_retry(model, messages, ..., wait=time.sleep):
    ...
    wait(2 ** attempt)
```

`time.sleep` really sleeps. A test that waits seven seconds is a test nobody runs. So
the function that waits is passed in — in tests, a fake one that just writes down how
long it was asked to wait. Same trick as `approve` on Monday and `model` since week 4.

### The provider SDKs already retry

Both official packages retry transient errors a couple of times on their own before
your code ever sees a `ModelError`. Yours is a second layer, for a run you do not want
to lose. Know both exist; do not multiply them into ten-minute hangs.

### A budget is a guard like any other

The step cap limits trips. It does not limit money: ten steps over a long history can
cost a hundred times what ten steps over a short one do. A **token budget** limits the
thing you actually pay for.

Check it at the same place as every other guard: after a reply, **before** doing more
work. If the model has already answered, return the answer — it is paid for. Only stop
when the run was about to continue.

| `stopped` | `answer` |
|---|---|
| `budget` | `I reached my token budget before finishing.` |

---

## Exercises

```bash
pytest week-07/day-4 -v
```

Copy `agent.py` and `guards.py` from day 3.

### 1. `retry.py`

| Function | Does |
|---|---|
| `call_with_retry(model, messages, system=None, tools=None, retries=2, wait=time.sleep)` | calls `model.chat` and returns the reply. On a **retryable** `ModelError`, waits `1`, then `2`, then `4` … seconds and tries again, up to `retries` extra times. A non-retryable error, or running out of retries, passes the error on |

### 2. `agent.py`

Add three arguments at the end:

```python
run_agent(..., token_budget=None, retries=2, wait=time.sleep)
```

- Call the model through `call_with_retry`, passing `retries` and `wait` along.
- After adding a reply's usage: if the model asked for tools **and** total tokens
  (input + output) are now over `token_budget`, stop with `budget`.
- `token_budget=None` means no limit.

---

## Predict-then-run

A run has `retries=2`. The model fails with a retryable error every single time. How
many times is `model.chat` called, how long does the run wait in total, and what is
`stopped`?

---

## Before you close the laptop

Commit, push, fill in the signal log.
