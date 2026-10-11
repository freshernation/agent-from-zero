# Sources

The job of a reading list is not to include everything. It is to say which handful of sources
deserve your attention, and which thousands you can ignore.

This is every reading in the course. The rule used to choose them: **the primary
source, from the people who built the thing, and nothing else.** No tutorials, no
video courses, no "ultimate guides". When a day's README links a page, it names the
section to read; the rest of the page can wait.

Documentation moves. If a link is dead, search the site for the page title.

---

## The five worth reading twice

If you read nothing else in the whole course, read these.

| | Why |
|---|---|
| [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — Anthropic | The clearest statement of what an agent is, when not to build one, and why simple beats clever. Week 6, and again in week 8 |
| [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) — Anthropic | Tool descriptions and tool results are where agents succeed or fail. Weeks 6 and 8 |
| [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic | What goes in the message list, and what to do when it is too long. Week 7 |
| [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Anthropic | How to know whether an agent works. Week 7 |
| [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — OpenAI | The same ground from the other major provider: design foundations, guardrails, human intervention. Weeks 6 and 7 |

---

## Weeks 1–3 — Python

One source: [the official Python tutorial](https://docs.python.org/3/tutorial/). Each
day links the section it needs. You will read perhaps a fifth of it in this course,
and that is the right amount.

Plus one page for week 3: [pytest — get started](https://docs.pytest.org/en/stable/getting-started.html).

**Ignore for now:** every "learn Python in X hours" video, any site that lets you
type code into a browser, and any chapter on classes.

## Week 4 — Talking to a model

Read your own provider's pages closely and skim the other's on Thursday.

| Claude | OpenAI |
|---|---|
| [Working with the Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages) | [Text generation](https://platform.openai.com/docs/guides/text) |
| [Messages API reference](https://platform.claude.com/docs/en/api/messages) | [Chat Completions API reference](https://platform.openai.com/docs/api-reference/chat/create) |
| [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) | [Pricing](https://platform.openai.com/docs/pricing) |
| [Increase output consistency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/increase-consistency) | [Conversation state](https://platform.openai.com/docs/guides/conversation-state) |

**Ignore for now:** prompt-engineering courses and prompt "templates". You will learn
more from one afternoon of changing a system prompt and watching what happens.

## Week 5 — Tools

| Claude | OpenAI |
|---|---|
| [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) | [Function calling](https://platform.openai.com/docs/guides/function-calling) |
| [How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works) | |
| [How to implement tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use) | |
| [Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) | |

**Ignore for now:** anything describing a "tool runner", an "agents SDK" or MCP. They
are all the thing you are about to write by hand.

## Week 6 — The loop

The first two of "the five" above. Nothing else. The reading this week is your own
trace.

**Ignore for now:** every framework's documentation. All of it.

## Week 7 — Trust it

| | |
|---|---|
| [LLM01: Prompt injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — OWASP | The standard reference for the attack |
| [The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) — Simon Willison | The single most useful way to think about when an agent is dangerous |
| [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) — Claude | What the limit is and what counts toward it |
| [Define success](https://platform.claude.com/docs/en/test-and-evaluate/define-success) and [Develop test cases](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) — Claude | Before you write an eval, say what passing means |
| [Errors](https://platform.claude.com/docs/en/api/errors), [Rate limits](https://platform.claude.com/docs/en/api/rate-limits) — Claude; [Rate limits](https://platform.openai.com/docs/guides/rate-limits) — OpenAI | Which failures are worth retrying |

**Ignore for now:** eval platforms and dashboards. A list of dictionaries and a
`for` loop is an eval harness.

## Week 8 — Your agent

Re-read the first two of "the five". Then read your own week 6 write-up.

---

## Finding a source yourself

When you need a source this page does not list, open `ai/source-finder.md`. It will find
three or four candidates and tell you which to ignore — and it is told to prefer
official documentation over everything else.
