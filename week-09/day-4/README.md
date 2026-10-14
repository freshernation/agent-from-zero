# Day 4 — Break it, fix it, write it down

> **By the end of today** you have attacked your own agent three times, recorded what
> happened, and written the page a stranger will read first.

---

## 1. Three attacks

Use `ai/editor.md` in its red-team mode — it will propose attacks; you run them
against a real model. At minimum:

1. **Injection.** Put an instruction inside your own data and ask an innocent question.
2. **Confusion.** Ask for something ambiguous that could be read as a dangerous action.
3. **Exhaustion.** Ask for something that cannot be finished, and watch which guard
   ends it and what it cost.

For each one, record in `EVAL_REPORT.md`: what you tried, the trace, what happened,
and what you changed. Then **turn each attack into an eval case**, so it is checked
forever.

If an attack succeeded and you could not fix it, say so. An honest *"this still gets
through one time in five, and here is why the damage is limited"* is a professional
sentence. A report with no failures in it is not believed.

## 2. Final eval run

Run the suite three times. Record all three scores.

## 3. `project/README.md`

This is the first thing anybody opens. A template is in the folder. It must let a
stranger run your agent in under five minutes, and it must be honest about what the
agent cannot do.

## 4. Rehearse

Run `ai/defend.md` on the project. Then practise the ten-minute demo once, out loud,
with a timer.

---

## Check it

```bash
pytest week-09/project -v
```

Everything green.

---

## Before you close the laptop

Commit, push. Check `.env` is not in the repository. Check that someone who clones it
fresh can run it — ideally by actually doing that, in a new folder.
