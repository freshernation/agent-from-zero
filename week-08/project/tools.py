# Week 8 - your tools.
#
#   <your tool functions>   at least four. Plain arguments in, a SENTENCE out.
#                           They never raise on bad input.
#
#   EMPTY                   the empty state of your data, usually [] or {}
#   reset(state)            replace everything in the data file with `state`
#   snapshot()              return the whole current state
#
#   SCHEMAS                 one schema per tool
#   TOOLS                   the dispatch table: name -> function
#   DANGEROUS               the set of tool names that need a human's yes
#
#   run_tool(tools, name, args)
#                           run one tool and return a string, whatever happens.
#                           You wrote this in week 5; the kit has carried it for
#                           you since. It is yours again now.
#
# The data lives in the file named by os.environ.get("DATA_FILE", "data.json").
# Read that INSIDE each function, not once at the top of the file.
