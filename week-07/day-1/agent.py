# Day 1 - the loop, with an approval gate.
#
# Copy your week-06/milestone/agent.py here, then add two arguments at the end:
#
#   run_agent(..., dangerous=None, approve=None)
#
#   - dangerous: a set of tool names. A call to one of them runs only if
#     approve(call) returns True.
#   - Otherwise it is NOT run, and its result is:
#         "Refused: the user did not approve delete_note."
#   - dangerous set but approve is None  ->  every dangerous call is refused.
#   - approve is called only for dangerous tools, once per call.
#
# Run the calls one at a time with kit.run_tool, instead of kit.run_calls.
