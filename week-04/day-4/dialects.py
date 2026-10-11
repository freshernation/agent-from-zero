# Day 4 - the same request and reply, in each provider's own shape.
# Plain dictionaries only. No network, no model.
#
#   claude_request(model_name, messages, system=None, max_tokens=1024)
#       {"model": ..., "max_tokens": ..., "system": ..., "messages": [...]}
#       Leave "system" out entirely when there is none.
#
#   openai_request(model_name, messages, system=None)
#       {"model": ..., "messages": [...]}  with the system prompt as the FIRST
#       message when there is one. Must not change the list it was given.
#
#   claude_text(raw)      every "text" block in raw["content"], joined
#   openai_text(raw)      raw["choices"][0]["message"]["content"], or "" if None
#
#   neutral_stop(provider, raw)     "done" | "length" | "refused"
#       claude:  end_turn -> done,  max_tokens -> length,  refusal -> refused
#       openai:  stop -> done,      length -> length,      content_filter -> refused
#       anything else -> done
#
#   neutral_usage(provider, raw)    {"input": ..., "output": ...}
#       claude:  usage.input_tokens / usage.output_tokens
#       openai:  usage.prompt_tokens / usage.completion_tokens
