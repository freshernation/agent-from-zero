# Day 1 - the loop.
#
#   run_agent(model, task, schemas, tools, system=None, max_steps=10)
#
#       messages starts as one user message holding the task.
#       Loop, at most max_steps times:
#           ask the model (system prompt, tools offered)
#           append its turn
#           if it did not ask for tools  ->  finished
#           otherwise run the calls and append the results
#
#       Returns:
#           {"answer": <the model's text>, "stopped": "done",
#            "steps": <number of model calls>, "messages": messages}
#       or, when the cap ends the run:
#           {"answer": "I ran out of steps before finishing.",
#            "stopped": "max_steps", "steps": ..., "messages": messages}
#
# from kit import run_calls
