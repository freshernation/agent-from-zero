# Day 2 - a conversation is a list you keep resending.
#
#   send(model, history, text, system=None)
#       append the user's message, call the model with the WHOLE history,
#       append the model's turn (reply["message"]), return its text.
#       If the call raises ModelError: leave history exactly as it was, and
#       pass the error on.
#
#   turns(history)    how many user messages there are
#   reset(history)    empty THAT list
