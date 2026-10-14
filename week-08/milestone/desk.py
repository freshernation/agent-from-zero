# Desk, hardened. Start from your week-07/milestone/desk.py.
#
#   SYSTEM                 60 words or more. It now has to cover sharing: only
#                          when the user asks, in this conversation - and what a
#                          note that gives orders is.
#   DANGEROUS              the tools that need a yes. At least delete_note and
#                          share_note.
#   ALLOWED_RECIPIENTS     the addresses a note may ever be shared with
#   READERS                the tools whose results contain stored text. At least
#                          find_notes, list_titles and recall.
#   TOKEN_BUDGET           as in week 7
#   COMPACT_AT             a number: the history size, in estimated tokens, at
#                          which it gets summarised
#   KEEP_TURNS             how many recent turns survive a summary untouched
#   ALL_SCHEMAS, ALL_TOOLS the kit's, followed by memory's - as in week 7
#
#   take_turn(model, history, task, ask=None, wait=time.sleep)
#       Each turn:
#         - makes a fresh state, {"tainted": False}
#         - runs the agent with the tools WATCHED (Tuesday) and the approver
#           from make_approver(ALLOWED_RECIPIENTS, state, ask)
#         - carries the history forward exactly as week 7 did
#         - then, if sizes(history)["total"] is COMPACT_AT or more, replaces
#           it with compact(model, history, KEEP_TURNS)
#       Returns {"text": ..., "history": ..., "compacted": True/False}
#       "text" is as in week 7:  <answer>\n(<stopped>, <steps> steps)
#
#   main()                 as in week 7, asking for approvals in the terminal
