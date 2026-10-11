# Day 4 - tool calls in each provider's own shape. Plain dictionaries only.
#
#   claude_tool(schema)     {"name", "description", "input_schema"}
#   openai_tool(schema)     {"type": "function",
#                            "function": {"name", "description", "parameters"}}
#
#   claude_calls(raw)       neutral calls [{"id", "name", "args"}] from the
#                           tool_use blocks in raw["content"]
#   openai_calls(raw)       the same from raw["choices"][0]["message"]["tool_calls"]
#                           - which may be missing or None
#                           - whose arguments are a JSON STRING; unparseable -> {}
#
#   claude_results(tool_messages)
#       ONE message: {"role": "user", "content": [
#           {"type": "tool_result", "tool_use_id": ..., "content": ...}, ...]}
#   openai_results(tool_messages)
#       a list: [{"role": "tool", "tool_call_id": ..., "content": ...}, ...]
