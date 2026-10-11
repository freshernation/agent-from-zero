# Day 3 - three small guards.
#
#   signature(call)
#       a string that is identical for two calls with the same name and the
#       same args - whatever order the args are in.   (json.dumps, sort_keys=True)
#
#   is_repeating(signatures, limit=3)
#       True if the LAST signature in the list appears at least `limit` times.
#
#   clip(text, limit=2000)
#       unchanged if it fits; otherwise the first `limit` characters followed by
#       "... [3000 more characters cut]"
