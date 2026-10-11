# Day 3 - the loop, hardened.
#
# Copy your day-2 agent.py here, then grow it:
#
#   run_agent(model, task, schemas, tools, system=None,
#             max_steps=10, repeat_limit=3, result_limit=2000)
#
#   stopped       answer
#   -----------   ----------------------------------------------
#   done          the model's text
#   max_steps     "I ran out of steps before finishing."
#   repeating     "I kept repeating the same step, so I stopped."
#   length        the model's text + " [cut off]"
#   refused       "The model declined this request."
#   error         "The model is unavailable: <message>"     (ModelError)
#
#   - Check for repeating BEFORE running the tools.
#   - Clip every tool result to result_limit, in the messages and the trace.
#   - A ModelError does not count as a step.
#   - Every ending except done adds a last trace event:
#         {"step": <steps>, "kind": "stop", "reason": <stopped>}
