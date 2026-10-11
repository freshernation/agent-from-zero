# Week 3 — Storage, failure, and pieces

> **Destination**
> Build a program in several files that remembers things between runs and does not
> fall over when something goes wrong.

Three things separate a script from a program: it **keeps** its data, it **survives**
bad input, and it is **split** into parts you can test one at a time. One day each.

This is the last week with no model in it. Everything you build here — the calculator,
the notes store — is something the agent will be handed in week 5.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Save Python data to a file as JSON and read it back |
| Tue | `day-2/` | Catch an error, raise one on purpose, and write a tool that never crashes |
| Wed | `day-3/` | Split code across files, and write your own tests |
| Thu | `day-4/` | Debug files, JSON, and swallowed errors |
| Fri | `milestone/` | Ship **Project 1** — a notes app that persists, in four files |

---

## The rule that starts on Tuesday and never ends

> **A tool returns a string. Always. Even when it fails.**

`"391"` when it worked. `"Error: Cannot divide by zero"` when it did not. A tool that
raises an exception at an agent ends the agent. A tool that *says* what went wrong
gives the model a chance to try something else — and recovering from a mistake is the
entire reason to use an agent instead of a script.

---

## Outside-view question

> *How does a pilot's checklist deal with things going wrong, and what is the
> difference between that and a `try` / `except`?*

---

## Project 1

A command-line notes app: add, list, find, delete, and a calculator, with everything
saved to a JSON file. Four files, each with one job. Spec in `milestone/README.md`.
