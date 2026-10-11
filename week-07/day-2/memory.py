# Day 2 - three kinds of memory.
#
#   estimate_tokens(messages)     total characters in every "content", // 4
#
#   trim(messages, max_turns)     the last max_turns turns. A turn starts at
#                                 each user message.
#                                 - nothing to cut: the same messages, untouched
#                                 - something cut: COPIES of the kept messages,
#                                   without any key that starts with "_"
#                                 - never changes its input
#
#   carry(history, result, max_turns=10)
#                                 result ended "done": trim(result["messages"], max_turns)
#                                 otherwise: history, unchanged
#
#   remember(fact)                append to the JSON list in MEMORY_FILE
#                                 (default memory.json).
#                                 "Remembered."  or  "I already know that."
#   recall(word="")               matching facts, one per line; all of them
#                                 when word is "".
#                                 "Nothing remembered yet."
#                                 "Nothing remembered about 'x'."
#
#   MEMORY_SCHEMAS                two schemas: remember(fact), recall(word)
#                                 - word is optional
#   MEMORY_TOOLS                  {"remember": remember, "recall": recall}
