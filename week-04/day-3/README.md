# Day 3 — Cost, cut-offs, and output you can trust

> **By the end of today** you can put a price on a conversation, notice when a reply
> was cut short, and get structured data out of a model without believing it blindly.

---

## Read first

- [ ] Claude — [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) — the model table only · 5 min
- [ ] OpenAI — [Pricing](https://platform.openai.com/docs/pricing) — the model table only · 5 min
- [ ] Claude — [Increase output consistency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency) · 10 min

---

## What you need to know

### Pricing is per million tokens, in two prices

Input and output are priced separately, and output costs several times more.

```python
usage = {"input": 1200, "output": 300}
price_in, price_out = 4.00, 20.00            # dollars per MILLION tokens

cost = usage["input"] / 1_000_000 * price_in + usage["output"] / 1_000_000 * price_out
# 0.0048 + 0.006 = $0.0108
```

Look up the real prices for your model on the pages above — they change.

On models that think before answering, the thinking is billed as **output** tokens even
though you never see it. A one-word answer can cost a few hundred output tokens.

### `stop == "length"`

Every call has a ceiling on how much the model may write (`max_tokens`). Hit it and the
reply simply ends, mid-sentence, with `stop` set to `"length"`. Nothing raises. If you
never look at `stop`, you will one day save half a paragraph and call it an answer.

### Asking for JSON

You often want data, not prose: *pull the title and the body out of this sentence.*
You ask in the system prompt:

```python
SYSTEM = (
    "Extract a note from the user's sentence. Reply with ONLY a JSON object with "
    'two keys: "title" (a few words) and "body" (the detail). No other text.'
)
```

And then you do not trust what comes back. In practice you get all of these:

```
{"title": "milk", "body": "two litres"}                       <- what you asked for
Sure! Here is the note:\n{"title": "milk", "body": "..."}     <- wrapped in chat
```json\n{"title": "milk", "body": "..."}\n```                <- wrapped in a code fence
{"title": "milk"}                                             <- a key missing
I'm not sure what you mean.                                   <- not JSON at all
```

### Parse, validate, retry

1. **Parse** — find the JSON inside whatever arrived. Taking everything from the first
   `{` to the last `}` handles the first three cases at once.
2. **Validate** — is it a dictionary? Are the keys you need there, with the right type?
3. **Retry once** — if not, tell the model what was wrong, in the same conversation,
   and ask again. Once. A model that fails twice will fail a third time.

```python
text.find("{")       # position of the first {   (-1 if there is none)
text.rfind("}")      # position of the last }
text[start:end + 1]  # the slice between them, inclusive
```

Both providers also offer a **structured output** feature that guarantees valid JSON.
Use it in real projects. Today you do it by hand, because validating what a model gives
you is a habit you need for the rest of the course — a tool call is a model handing
you JSON too.

---

## Exercises

```bash
pytest week-04/day-3 -v
```

### 1. `meter.py`

| Function | Returns |
|---|---|
| `cost(usage, price_in, price_out)` | dollars, as a number. Prices are per million tokens |
| `total_usage(replies)` | one `{"input": ..., "output": ...}` summing a list of replies |
| `was_cut_off(reply)` | `True` if the reply stopped for length |

### 2. `extract.py`

| Function | Returns |
|---|---|
| `parse_json(text)` | the dictionary inside the text, or `None` if there is no JSON object there |
| `is_note(data)` | `True` if `data` is a dict with a non-empty string `"title"` and a string `"body"` |
| `extract_note(model, sentence)` | a valid note dict, or `None`. One call if the first answer is valid. Otherwise **one** retry in the same conversation, then give up |

For the retry: append the model's turn, append a user message saying what was wrong,
and call again. The model should see its own bad answer.

---

## Predict-then-run

With a real provider, call `extract_note` on *"don't forget the dentist on Friday at
3"* five times. Do you get the same title five times? Does it matter?

---

## Before you close the laptop

Commit, push, fill in the signal log.
