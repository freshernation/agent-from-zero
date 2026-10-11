# Day 2 - reading a trace.
#
#   format_event(event)     one line:
#       [1] say: Now the yearly figure.
#       [1] call calculate({"expression": "1450 * 12"})       <- json.dumps(args)
#       [1] result calculate: 17400
#       [2] answer: That is 17400 a year.
#       [4] stop: max_steps
#
#   format_trace(trace)     every event's line, joined with newlines
#   summary(result)         "done in 3 steps (300 tokens in, 60 out)"
