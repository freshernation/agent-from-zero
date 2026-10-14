# Week 8 — Harden it

> **Destination**
> A Desk that survives a long conversation, a note that gives orders, and a careless
> change — with a number for each.

Last week you made Desk safe enough to trust with your own notes file. This week it
gets one new ability, and that ability is the reason for the week: **it can send a
note to somebody.**

Until now the worst Desk could do was damage a file on your laptop. Now something can
leave.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | See what is filling the model's window, and shrink it without breaking the conversation |
| Tue | `day-2/` | Stop a note leaving for an address nobody chose — in code, not in the prompt |
| Wed | `day-3/` | Attack your own agent on purpose, and report how often an attack works |
| Thu | `day-4/` | Check *which* note a tool was aimed at, and catch a change that breaks something that worked |
| Fri | `milestone/` | Ship a hardened Desk, with a threat model and the numbers |

---

## Four ways last week's Desk falls short

One per day. None of them is a bug in what you wrote.

1. **It forgets by throwing away.** Week 7's `trim` drops the oldest turns whole. The
   title of the note you saved at the start is gone with them.
2. **Its gate asks a person, and a person says yes.** Approval works for a delete you
   can see. It does not work when a note has quietly changed where something is sent.
3. **You tried three attacks by hand.** Three is not a measurement, and "it did not
   work when I tried" is week 7's "it worked when I tried", pointing the other way.
4. **Its evals pass a run that deleted the wrong note.** They check that
   `delete_note` was called. They do not check what it was called on.

---

## One new piece of Python

Tuesday needs **a function that builds a function**. You have passed functions as
arguments since week 7. This is the other half: writing a function whose job is to
return one, with something remembered inside it. It is the last new idea in the
course, and it is ten lines.

---

## Given to you

`kit.py`, with one more tool than last week: `share_note(title, to)`. Nothing is
really sent. A shared note is written to an **outbox** file, so you — and the tests —
can see exactly what went out and to whom.

---

## Outside-view question

> *A hospital pharmacist will hand over most medicines on a doctor's signature, and
> some only after a second pharmacist has checked. Who decided which are which, and
> what would you want to know before putting a tool on your agent's second list?*
