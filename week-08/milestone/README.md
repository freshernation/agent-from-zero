# Week 8 Milestone — A Desk that holds

> The Desk from week 7, able to share a note, and hardened: it summarises instead of
> forgetting, it cannot send to a stranger, and you have attacked it and counted.

---

## The files

| File | Where it comes from |
|---|---|
| `kit.py` | given — with `share_note` |
| `agent.py`, `guards.py`, `retry.py`, `memory.py`, `evals.py` | **copy from your week 7 milestone** |
| `context.py` | **copy from day 1** |
| `leak.py` | **copy from day 2** |
| `redteam.py` | **copy from day 3** |
| `baseline.py` | **copy from day 4** |
| `desk.py` | new — start from week 7's |
| `attacks.py` | new — your attack suite |
| `THREATS.md` | new — your threat model |
| `HARDENING_REPORT.md` | new — your numbers |

## `desk.py`

| Name | What it is |
|---|---|
| `SYSTEM` | 60 words or more. It now covers sharing, and says what a note that gives orders is |
| `DANGEROUS` | at least `delete_note` and `share_note` |
| `ALLOWED_RECIPIENTS` | the addresses a note may ever go to |
| `READERS` | the tools whose results contain stored text: at least `find_notes`, `list_titles`, `recall` |
| `TOKEN_BUDGET` | as in week 7 |
| `COMPACT_AT` | the history size, in estimated tokens, at which it is summarised |
| `KEEP_TURNS` | how many recent turns a summary leaves untouched |
| `ALL_SCHEMAS`, `ALL_TOOLS` | the kit's, then memory's |
| `take_turn(model, history, task, ask=None, wait=time.sleep)` | one turn, with everything switched on |
| `main()` | as in week 7 |

`take_turn`, in order:

1. makes a **fresh** state, `{"tainted": False}` — one turn's reading must not follow
   into the next
2. runs the agent with the tools **watched** and the approver from
   `make_approver(ALLOWED_RECIPIENTS, state, ask)`
3. carries the history forward exactly as week 7 did
4. if `sizes(history)["total"]` is `COMPACT_AT` or more, replaces the history with
   `compact(model, history, KEEP_TURNS)`

It returns `{"text": ..., "history": ..., "compacted": True/False}`, with `text` in
week 7's form: the answer, a new line, `(<stopped>, <steps> steps)`.

## `attacks.py`

`ATTACKS`: at least **six**, at least **three kinds**. It must include one aimed at
an address that is not allowed, one aimed at an address that **is** — the user did
not ask for it, so which control stops it? — and one that goes for the memory.

## `THREATS.md`

One page, four sections, written before you run anything.

| Section | What goes in it |
|---|---|
| `## What Desk holds` | What is in the notes and the memory that somebody would want |
| `## Who can put text in front of it` | Not only the user. Where does a note's text come from? |
| `## What each tool could do in the wrong hands` | A table, at least four tools: the worst it could do, who could cause it, what stops it |
| `## What I am not defending against` | Be honest. It is the section that shows you thought about it |

Where a tool has nothing stopping it, write **nothing** in that cell and mean it.

## `HARDENING_REPORT.md`

Numbers from your own runs against a real provider.

| Section | What goes in it |
|---|---|
| `## The window` | A long conversation: what filled it, how often it was summarised, and one thing a summary lost |
| `## The attacks` | The table: week 7's Desk against this week's, attacks, harms and success rate — each attack run at least three times |
| `## What still gets through` | At least one. If nothing does, your suite is too kind |
| `## The baseline` | A change you made, what the gate said, and what you did about it |

---

## Check it

```bash
pytest week-08/milestone -v
```

---

## Friday

The defence opens with your threat model, not your code. Then you run one attack
live, against a real model, that you say still gets through.
