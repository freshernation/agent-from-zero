# Day 2 - a calculator that is safe to hand to a stranger.
#
#   parse_int(text)              the whole number in the text, or None
#
#   calculate(expression)        the result as a number. Raises ValueError with:
#       "Unsafe expression"        anything but digits, spaces and + - * / ( ) .
#                                  and also any **
#       "Cannot divide by zero"
#       "Not a calculation"        safe characters, but not arithmetic ("2 +", "")
#
#   calculate_tool(expression)   NEVER raises. Returns a string either way:
#                                "391"   or   "Error: Unsafe expression"
#
# Check the characters BEFORE you eval.
