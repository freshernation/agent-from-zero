# Day 3 - evals: tasks with outcomes you can check.
#
#   tools_called(result)
#       names of the tools the model asked for, in order (from the trace)
#
#   check(result, expect, titles)
#       a list of failure sentences; [] means pass. Only keys present in
#       `expect` are checked, in this order:
#
#       "stopped"          stopped: expected 'done', got 'max_steps'
#       "answer_contains"  answer does not contain '17400'        (any capitals)
#       "calls"            did not call calculate                 (one per missing)
#       "never_calls"      called delete_note                     (one per used)
#       "max_steps"        took 7 steps, more than 4
#       "titles"           notes: expected ['milk'], got ['eggs', 'milk']
#                          (both sorted; order does not matter)
#
#   run_case(model, case, schemas, tools, system=None, dangerous=None, approve=None)
#       write case.get("notes", []) to the notes file, run the agent on
#       case["task"], then return
#       {"name": ..., "passed": True/False, "failures": [...], "steps": ...}
#
#   report(outcomes)
#       PASS add a note
#       FAIL delete one of three: did not call delete_note; notes: expected ...
#       1/2 passed
#
# The notes file is os.environ.get("NOTES_FILE", "notes.json").
