# Week 6 — The loop

> **Destination**
> Hand-write the loop that every agent framework is hiding, and know exactly why it
> stops.

This is the keystone week. Everything before it was preparation and everything after
it is elaboration.

---

## The whole idea, up front

You already wrote the agent loop. Twice. It is week 1's chatbot and week 4's assistant:

```
read a message  ->  decide  ->  respond  ->  go round again
```

Last Friday, Desk could use tools **once** per turn and then had to give up. An agent
removes that limit, and that is all it does:

1. **"decide"** is the model. If it asks for tools, run them, tell it what happened,
   and **ask it again**.
2. **"go round again"** gets a **stopping condition**, because now the loop can run
   with no human in it.

That is the entire difference between a chat assistant and an agent. There is no third
thing.

```
            +------------------------------------------+
            |                                          |
            v                                          |
   messages --> [ model ] --> asked for tools? -- yes --> run them, append results
                                   |
                                   no
                                   |
                                   v
                                answer            (and one more exit: out of steps)
```

Draw that from memory by Friday. It is, almost word for word, an interview question.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Write the loop, end to end, with a cap on it |
| Tue | `day-2/` | Watch it think: a trace of every step, and what it cost |
| Wed | `day-3/` | Survive tools that fail, loops that repeat, and replies that are cut off |
| Thu | `day-4/` | Debug an agent that is wrong without crashing |
| Fri | `milestone/` | Ship **Project 2** — an agent with no framework, and the write-up |

---

## `kit.py` is given

Each folder has a `kit.py`: last week's tools, schemas and dispatch in one file. This
week you write exactly one thing — `run_agent` — and you write it three times, each
day's version growing out of the last.

---

## An agent has two kinds of exit

**It finished.** The model answered without asking for a tool.

**You stopped it.** It hit the step cap, or kept repeating itself, or the model failed.

A loop with only the first exit is a way to spend money until someone notices. Every
version of `run_agent` you write this week has both, from the first line.

---

## Project 2

A working agent with at least five tools, a step cap, repeat detection, a trace, and a
write-up explaining the loop **in your own words**. That write-up is the artefact that
makes an interviewer sit up — almost nobody who uses agents can say what is underneath.

---

## Outside-view question

> *How does an air traffic controller decide when to stop giving a pilot instructions,
> and what does that have in common with a step cap?*

---

## The fence is absolute this week

No frameworks. Not one. Read `FENCE.md`.
