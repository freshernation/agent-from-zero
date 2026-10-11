# Day 2 - running what the model asked for.
#
#   TOOLS                     dict: tool name -> function. All five from toolbox.py.
#
#   run_tool(name, args)      run it; return the result AS A STRING. Never raises.
#                             "Error: unknown tool 'xyz'"         name not in TOOLS
#                             "Error: TypeError: <message>"       anything that goes
#                                                                 wrong while running
#
#   run_calls(tool_calls)     one message per call, in order:
#                             {"role": "tool", "tool_call_id": <id>, "content": <result>}
