# Week 7 Milestone - your eval suite.
#
#   CASES   a list of at least six cases:
#
#       {"name": "...",
#        "notes": [{"title": "...", "body": "..."}],      # optional starting state
#        "task": "...",
#        "user_approves": True,                           # optional; default no
#        "expect": {"stopped": ..., "answer_contains": ..., "calls": [...],
#                   "never_calls": [...], "max_steps": ..., "titles": [...]}}
#
#   Between them they must include: a case with starting notes, a case that
#   checks titles, a case that uses never_calls, and a case where the expected
#   titles are the same as the starting titles.
