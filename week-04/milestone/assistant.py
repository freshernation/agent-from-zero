# Week 4 Milestone - Desk can talk
# Author:
#
#   new_session(system)
#       {"system": system, "history": [], "usage": {"input": 0, "output": 0}}
#
#   handle(model, session, line)    the reply, as a string. No printing.
#       (empty)    "Say something."
#       /turns     "2 turns so far."
#       /cost      "Tokens: 40 in, 12 out. Cost: $0.0004"
#       /reset     empties the history, keeps the usage: "Conversation cleared."
#       anything else: send it to the model (system prompt + whole history),
#                      add the tokens to session["usage"], return the text.
#           cut off (stop == "length")  ->  the text + " [cut off]"
#           ModelError                  ->  "The model is unavailable: <message>"
#                                           and the history is left as it was
#
#   main()   connect(); loop on "You: "; print "Desk: <reply>";
#            on quit print the /cost line, then "Bye."

# Dollars per MILLION tokens. Replace with your model's real prices.
PRICE_IN = 4.00
PRICE_OUT = 20.00
