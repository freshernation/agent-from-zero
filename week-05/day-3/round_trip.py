# Day 3 - one full round trip.
#
#   answer(model, schemas, question, system=None)
#       1. ask the model, offering the tools
#       2. if it did not ask for tools, return its text
#       3. append its turn, run every call it made, append the results
#       4. ask again (tools still offered) and return that text
#       If it asks for tools a SECOND time, return:
#           "I could not finish that in one step."
