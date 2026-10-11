# What this course does not teach

The most valuable part of any course plan is the cut list. Every item below is a real thing
agent builders know, and every one of them is out.

**Python**

- Classes, inheritance, decorators, generators, comprehensions, type hints
- `async` / `await`, threads, running tools in parallel
- Packaging, virtual-environment tooling beyond `venv`, linters and formatters

**Models**

- How a language model works inside; training and fine-tuning
- Streaming responses, images and audio, prompt caching, batch APIs
- The providers' own structured-output and tool-runner helpers
- Model-graded evals ("LLM as judge")

**Agents**

- **Every framework** — LangChain, LangGraph, CrewAI, AutoGen, the OpenAI Agents SDK,
  the Claude Agent SDK
- Multi-agent systems, planners, sub-agents
- Retrieval: embeddings, vector stores, RAG
- MCP, and connecting to other people's tools
- Web browsing, code execution, sandboxes
- Deployment, web front ends, databases, authentication, observability platforms

---

## Why

Every item here is learnable in about a week **once you can write the loop** — and
none of them teaches you the loop. Most of them hide it.

A student who starts with a framework can build an impressive demo on day two and
cannot debug it on day three, because they do not know what it is doing. A student who
has written the loop reads a framework's source and recognises it.

Say this out loud in week 1. Students who know *why* something was cut stop worrying
that they are missing it, and that worry is a major cause of drift in week five.

---

## What to add afterwards, in order

If you finish and want more, roughly the order that pays back:

1. **Classes.** Your week 7 `run_agent` takes fourteen arguments. A class is the fix,
   and you now have a real reason to want one.
2. **The providers' own packages**, used directly — streaming, structured outputs,
   prompt caching. You have already written the translation layer; this is reading
   the documentation for the other side of it.
3. **Retrieval.** Give the agent a `search_documents` tool over your own files. It is
   one more tool, and the interesting part is measuring whether it helped — which
   week 7 taught you to do.
4. **One framework.** Rebuild Project 2 in it, then write down what it bought you and
   what it took away. You are now one of the few people who can write that paragraph.
5. **MCP.** A standard way to offer tools to an agent. It will look like your
   `SCHEMAS` and `TOOLS`, moved to another process.
6. **A sandbox**, and then tools that are actually dangerous: a shell, a browser.
7. **Deployment.** Put it behind an HTTP API, with traces you can search.
8. **Multi-agent.** Last, and only when a single agent with good tools has measurably
   failed at the task.
