# An agent is allowed 10 steps. Once it has USED 10, it must stop.
# With used = 10 this should print:  Stop
# With used = 9 it should print:     Keep going
used = 10
limit = 10

if used > limit:
    print("Stop")
else:
    print("Keep going")
