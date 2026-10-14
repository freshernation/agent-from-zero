# Day 4 - evals that hold the line.
#
#   called_with(result)
#       every tool the model asked for, with its arguments, in order:
#       [{"name": "delete_note", "args": {"title": "eggs"}}, ...]
#
#   check_args(result, expected)
#       `expected` maps a tool name to the arguments it must have been called
#       with:  {"delete_note": {"title": "eggs"}}
#       Failures as sentences; [] means pass. For each tool, in the order given:
#
#       never called at all        did not call delete_note
#       called, but no call has    delete_note: title expected 'eggs', got 'milk'
#       every expected argument    (one sentence per wrong argument of the LAST
#                                  call to that tool; a missing argument is None)
#
#       A tool passes if ANY one of its calls has every expected argument.
#       Extra arguments do not matter.
#
#   freeze(name, task, notes, result, titles)
#       an eval case that pins down what a run did:
#       {"name": name, "task": task, "notes": notes,
#        "expect": {"stopped": <how the run stopped>,
#                   "calls": <each tool called, once, in first-use order>,
#                   "titles": <titles, sorted>}}
#
#   save_baseline(path, outcomes)
#       write {"case name": True/False, ...} to the file as JSON
#   load_baseline(path)
#       read it back. {} if the file is not there.
#
#   regressions(baseline, outcomes)
#       names of the cases that PASSED in the baseline and FAIL now, in the
#       order of `outcomes`. A case that was already failing is not one.
#       A case that is new is not one.
#
#   gate(baseline, outcomes)
#       {"ok": <no regressions>, "regressions": [...],
#        "new": <names not in the baseline>,
#        "before": "5/6", "after": "4/6"}
#
#   exit_code(result)
#       0 when ok, 1 when not
#
# `outcomes` is what week 7's run_case returns, collected in a list.
