# Week 5 Milestone - Desk with hands
# Author:
#
#   SYSTEM    your system prompt. Who Desk is, that it has tools for the user's
#             notes, and at least one rule about care. 25 words or more.
#
#   respond(model, history, text)    one turn; returns the reply. No printing.
#       1. append the user's message
#       2. call the model: whole history, SYSTEM, the tools
#       3. if it asked for tools: append its turn, run the calls, append the
#          results, call once more
#       4. append the final turn; return its text
#
#       asks for tools a SECOND time  ->  do NOT append that turn; return
#                                         "I could not finish that in one step."
#       ModelError on the first call  ->  remove the user's message; return
#                                         "The model is unavailable: <message>"
#
#   main()    connect(); loop on "You: "; print "Desk: <reply>"; quit -> "Bye."
