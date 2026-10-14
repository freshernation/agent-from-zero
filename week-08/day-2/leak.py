# Day 2 - what can leave, and who decides.
#
# kit.py has a new tool this week: share_note(title, to). Read it first.
#
#   allowed_recipient(to, allowed)
#       True when the address is in `allowed`, ignoring capitals and
#       surrounding spaces
#
#   watched(function, name, readers, state)
#       returns a NEW FUNCTION. Calling it with any keyword arguments:
#         - sets state["tainted"] = True if `name` is in `readers`
#         - then calls `function` with those arguments and returns the result
#
#   watch(tools, readers, state)
#       a NEW dispatch table with every tool replaced by its watched version.
#       The original table is not changed.
#
#   make_approver(allowed, state, ask=None)
#       returns a function approve(call) for run_agent. Its rules:
#
#       share_note to an address NOT in `allowed`    False. Never asks.
#       share_note to an allowed address,
#           and state["tainted"] is False            True. No need to ask.
#       anything else                                ask(call) is True -
#                                                    and False if ask is None
#
# `state` is a dictionary you make: {"tainted": False}. The same dictionary
# goes to watch and to make_approver, which is how one finds out what the
# other saw.
