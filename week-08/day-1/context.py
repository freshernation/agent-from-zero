# Day 1 - what is in the window, and what to do when there is too much of it.
#
#   tokens(text)
#       len(text) // 4 - week 7's estimate, for one string
#
#   sizes(messages)
#       estimated tokens by role, and in all:
#       {"user": 12, "assistant": 40, "tool": 900, "total": 952}
#       A role with no messages is 0.
#
#   shorten_old_results(messages, keep_last=2, limit=200)
#       a NEW list of COPIES. Every "tool" message except the last `keep_last`
#       of them has content longer than `limit` cut to its first `limit`
#       characters, followed by
#           " [shortened: 1800 characters removed]"
#       No message is ever dropped, and no other message is changed.
#
#   split_turns(messages)
#       a list of turns. A turn is a user message and everything after it up
#       to the next user message.
#
#   SUMMARY_SYSTEM
#       the instructions for the model that writes the summary. 30 words or
#       more. Say what must survive: titles, what was saved, deleted or
#       shared, and what the user said about themselves.
#
#   transcript(messages)
#       one line per message:   user: Delete the eggs note.
#
#   summarise(model, messages)
#       ONE model call: a single user message holding the transcript, with
#       system=SUMMARY_SYSTEM and no tools. Returns the reply's text.
#
#   compact(model, messages, keep_turns=3)
#       keep_turns or fewer turns: a copy of the list, and NO model call.
#       Otherwise: summarise every turn before the last `keep_turns`, and
#       return copies of the kept turns - without any key starting with "_",
#       exactly as week 7's trim - where the FIRST kept message's content has
#       become
#           "Summary of the conversation so far: <summary>\n\n<what it said>"
#
#   should_compact(used, window, fraction=0.5)
#       True when `used` is at least that fraction of the window
#
#   tools_size(tools)
#       len(json.dumps(tools)) // 4 - the tool descriptions, as the estimate would
#       count them. 0 for no tools.
#
#   estimate(messages, system=None, tools=None)
#       sizes(messages)["total"], plus tokens(system), plus tools_size(tools):
#       everything a request carries, not just the conversation
#
#   window_used(model, messages, system=None, tools=None)
#       ask the provider: {"tokens": model.count_tokens(messages, system=system,
#       tools=tools), "source": "counted"}. If the model has no count_tokens, or it
#       raises ModelError, fall back to {"tokens": estimate(...), "source": "estimated"}.
#       Counting is free and is not a model call; the fallback is for when the
#       counter is unreachable, not a reason to skip it.
