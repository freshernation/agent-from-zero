# Week 6 — Friday defence · Project 2

**The most important defence in the course.** Budget the full hour and do not let it
get squeezed.

---

## Phase 0 — The paper test (3 min)

Before anything else. No laptop, no notes, no screen.

> *"Draw the agent loop."*

Boxes and arrows on paper. What you are looking for:

- the message list, and the fact that it **grows**
- the model call
- the **branch on `stop`** — this is the one that matters
- run tools → append results → go round
- an **exit that is not the answer** (the cap)

A student who can draw this in ninety seconds owns the week. One who cannot has typed
it. **This is also, almost verbatim, a question they will be asked in an interview** —
say so afterwards, whichever way it went.

## Phase 1 — Explain (8 min)

1. *"Does the model ever run your code?"*
2. *"Who decides how many steps a task takes? Point at the line where that decision
   is read."*
3. *"What is a step? If one reply asks for three tools, how many steps is that?"*
4. *"The model called `find_notes` with no arguments. Walk me through the next two
   trips round the loop."* — looking for: the error sentence goes back, the model
   retries, **nothing in their code changed**.
5. *"Why does the repeat check run before the tools and not after?"*

## Phase 2 — Mutate (12 min)

### A — *"Add a seventh ending: stop if the run has used more than 5,000 input tokens."*

Name the lines before typing. Looking for: checked after usage is added, a new
`stopped` value, a `stop` event in the trace — and the realisation that one more guard
is just one more `if` that returns.

### B — *"A tool now takes thirty seconds. What breaks?"*

Discussion only. Nothing crashes; the whole run blocks. Then: *"and if it never
returns?"* — the step cap does not help, because the loop is not going round. Looking
for the word **timeout**, and a decision about what the model is told when it fires.

### C — *"The model asks for `calculate` with `2+2`, gets `4`, and asks again. Three times. Walk me through what each of your guards does."*

Cap, repeat detection, clip. Which fires first, and why the repeat check is worth
having when the cap would eventually catch it anyway.

## Phase 3 — Debug (10 min)

Seed one before they arrive.

| Seed | Break | Probes |
|---|---|---|
| Easy | `result_limit` default 20 instead of 2000 | Reading a trace: every result is cut |
| Medium | `if reply["stop"] != "tools"` becomes `== "done"` only, with no `length` branch | Works until a cut-off reply, then the fake rejects the next call |
| Medium | drop `sort_keys=True` from the signature | Repeat detection misses reordered arguments |
| Hard | append the results **before** the assistant turn | The fake rejects it; can they read the message? |
| Nasty | `signatures.append(...)` moved after the tools run | Off by one: the tool runs a third time. Only one test notices. |

Ask of the **Nasty** one: *"The agent still worked. How would you have noticed in
production?"* — the trace, and the call count.

## Phase 4 — Live (10 min)

Against a real provider with `AGENT_TRACE=1`. Give it: *"Add milk, eggs and bread,
delete the eggs one, then tell me what is left."* Have the student **narrate the trace
as it scrolls**. Then ask for one change to the system prompt that would alter the
trace, make it, and run it again.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Paper** | Draws it in 90 seconds including the cap | Gets the shape, misses the exit | Cannot start |
| **Explain** | "The model decides; I only read `stop`" unprompted | Describes the flow correctly | Thinks the code plans the steps |
| **Mutate** | Places the new guard and names its trace event | Gets it working by running | Cannot find where an ending is decided |
| **Debug** | Reproduces, isolates, one change | Finds it | Guesses |
| **Live** | Predicts the next trace line before it appears | Explains each line after | Reads it aloud |

Pass is 3 in every phase. **A 1 on the paper test is a fail regardless of the rest** —
it is the one thing this week existed to produce.

---

## Then: read the write-up out loud

Ten minutes. Have them read `WRITEUP.md` to you, and stop them wherever a sentence
sounds like it came from somewhere else. Not as an accusation — as an edit. *"Say that
bit again in your own words"* improves the document and tells you what they own.

---

## Say this before they leave

> **You have built the thing every agent framework is built around. From here the
> code gets easier and the judgement gets harder: next week is not about making the
> agent work, it is about deciding what it should be allowed to do.**
