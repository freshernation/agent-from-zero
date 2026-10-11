# Day 2 - the loop, with a record of what it did.
#
# Copy your day-1 agent.py here, then add two keys to the result on BOTH exits:
#
#   "usage"   {"input": ..., "output": ...}  summed over every model call
#   "trace"   a list of events. Every event has "step" and "kind":
#
#       {"step": n, "kind": "say",    "text": ...}             text alongside tool calls
#       {"step": n, "kind": "call",   "name": ..., "args": ...}      one per call
#       {"step": n, "kind": "result", "name": ..., "content": ...}   one per result
#       {"step": n, "kind": "answer", "text": ...}             the model finished
#       {"step": n, "kind": "stop",   "reason": "max_steps"}   you ended the run
#
#   Within a step: say (if any text), then every call, then every result.
