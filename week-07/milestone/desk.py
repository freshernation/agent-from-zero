# Week 7 Milestone - a Desk you would trust
# Author:
#
#   SYSTEM         your system prompt. 40 words or more. Cover memory (when to
#                  remember, when to recall) and what to do when an action is
#                  refused.
#   DANGEROUS      the set of tool names that need approval. At least delete_note.
#   TOKEN_BUDGET   the most tokens one turn may use.
#   ALL_SCHEMAS    kit.SCHEMAS followed by MEMORY_SCHEMAS
#   ALL_TOOLS      one table: the kit's tools and the memory tools
#
#   take_turn(model, history, task, approve=None, wait=time.sleep)
#       run the agent once, continuing history, with SYSTEM, ALL_SCHEMAS,
#       ALL_TOOLS, DANGEROUS, TOKEN_BUDGET, approve and wait. Returns:
#           {"text": "<the answer>\n(done, 2 steps)",
#            "history": carry(history, result)}
#
#   main()   connect(); loop on "You: "; approve with approve_in_terminal;
#            print "Desk: <text>"; quit -> "Bye."
