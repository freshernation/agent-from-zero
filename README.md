# Agent From Zero

Eight weeks from your first line of Python to an AI agent you designed, built,
measured and can explain — with no framework underneath it.

You do not need to have programmed before. You do need about four hours a day.

Everything in this repo is aimed at one outcome: **you can draw the agent loop on a
whiteboard, and you have written every line of it.** If something looks missing, it
was cut on purpose — see `CUT_LIST.md`.

---

## The three rules

**1. The twenty-minute rule.**
Stuck? Struggle alone for twenty minutes. Then open the **tutor** (`ai/tutor.md`) —
never a plain chat, never "write this for me". Then, and only then, bring it to the
live hour. Log every stuck event in `logs/stuck-log.md`.

**2. You write every line for the first three weeks.**
Weeks 1–3 are AI-off for writing code. The AI is a tutor, not an author. Not a moral
position — decomposition and debugging are the two skills an agent builder needs most,
and they are exactly the two a model will quietly do for you if you let it.

From week 4 the AI may write code with you, and the rule that replaces it is:
**you may not commit a line you could not have written and cannot explain on Friday.**

**3. Nothing counts until the tests pass and it's pushed.**

---

## The eight weeks

| Week | | Milestone |
|---|---|---|
| 1 | Code is not magic | A rule-based chatbot — a loop with no AI in it |
| 2 | Names for actions, rows of things | A notes toolkit: four functions that return sentences |
| 3 | Storage, failure, and pieces | **Project 1** — a notes app that persists, in four files |
| 4 | Talking to a model | A chat assistant with memory and a cost meter, on any provider |
| 5 | Tools | The assistant can use your notes functions — one step at a time |
| 6 | **The loop** | **Project 2** — an agent from scratch, and the write-up |
| 7 | Trust it | The agent gated, remembering, budgeted — and measured with evals |
| 8 | Your agent | **Project 3** — an agent for a problem you chose, defended |

Week 6 is the keystone. Weeks 1–3 exist so that week 6 contains nothing unfamiliar:
the loop is week 1, the message list is week 2, the tools are weeks 2 and 3.

---

## One project, growing

You do not build eight unrelated things. You build one thing eight times.

```
week 1   a loop that reads, decides with an if-ladder, and responds
week 2   functions that add, list, find and delete notes
week 3   ...saved to a file, and safe against bad input
week 4   the if-ladder is replaced by a model
week 5   the model is handed the functions
week 6   the model is allowed to go round more than once        <- an agent
week 7   ...and is stopped from doing damage, and measured
week 8   the notes are replaced by a problem of your own
```

---

## Any provider

The course code talks to a model through one small layer, `llm/`, with three backends:

| | |
|---|---|
| `fake` | No key, no network, no cost. The default. Every test uses it. |
| `claude` | Anthropic's Claude |
| `openai` | OpenAI's models |

You choose with one line in `.env`. Twice — week 4 Thursday and week 5 Thursday — you
open that layer and write parts of it yourself, so you leave able to read either
provider's documentation.

---

## Daily rhythm

| | |
|---|---|
| **Live hour** | One hour with your instructor, five days a week |
| **Independent** | Four or more hours a day — where the learning actually happens |
| **Friday** | No new content. Defend, ship, retro. |

```bash
source .venv/bin/activate          # every session

pytest week-01/day-1 -v            # one day
pytest week-01 -v                  # one week
```

Tests are the grader. A green test means "this behaves correctly", not "this is good
code" — the **editor** (`ai/editor.md`) judges the second thing, and your instructor
judges both on Friday. Every test fails before you write anything.

---

## Map

| Path | What it is |
|---|---|
| `SETUP.md` | Day zero. Do this before anything else. |
| `week-01/` … `week-08/` | One folder per week: four days, a milestone, a fence, a defence |
| `llm/` | The model layer. Read it in week 4. |
| `ai/` | Your AI roles — planner, source finder, tutor, editor, outside view, defend |
| `SOURCES.md` | Every reading in the course, and why it was chosen |
| `CUT_LIST.md` | What this course deliberately does not teach, and what to learn next |
| `logs/stuck-log.md` | Every time you get stuck. Non-negotiable. |
| `logs/signal-log.md` | Your daily numbers. Two minutes at end of day. |

Each week has a `FENCE.md` listing what you have learned and what you have not. Paste
both lists into any AI role before you use it — it is what stops the model teaching
you something three weeks early and making your toolkit feel inadequate.

---

## The three projects

| | Week | Proves |
|---|---|---|
| **Desk, with a memory** | 3 | you can write Python, not assemble it |
| **An agent, from scratch** | 6 | you understand agents rather than importing them |
| **Your agent** | 8 | you can decide what an agent should and should not do |
