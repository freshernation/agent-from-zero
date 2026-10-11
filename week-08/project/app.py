# Week 8 - Project 3
# Author:
#
#   SYSTEM    your system prompt. 40 words or more.
#
#   take_turn(model, history, task, approve=None, wait=time.sleep)
#       run the agent once, continuing history, with SYSTEM and your SCHEMAS,
#       TOOLS and DANGEROUS. Returns:
#           {"text": "<the answer>\n(done, 2 steps)",
#            "history": carry(history, result)}
#
#   main()    connect(); loop on "You: "; approve with approve_in_terminal;
#             print the reply; quit -> "Bye."
