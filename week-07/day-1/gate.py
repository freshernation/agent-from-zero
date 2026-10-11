# Day 1 - putting a human between the model and anything it cannot undo.
#
#   only(schemas, names)
#       a NEW list of just the schemas whose name is in `names`,
#       in their original order
#
#   describe_call(call)
#       'delete_note({"title": "milk"})'          (json.dumps the args)
#
#   approve_in_terminal(call, ask=input)
#       calls ask('Allow delete_note({"title": "milk"})? [y/N] ')
#       True only if the answer is y or yes, in any capitals
