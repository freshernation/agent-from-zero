# Day 1 - describing functions to a model.
#
#   text_param(description)     {"type": "string", "description": description}
#
#   make_schema(name, description, properties, required)
#       {"name": name, "description": description,
#        "parameters": {"type": "object",
#                       "properties": properties, "required": required}}
#
#   SCHEMAS    a list of five schemas, in this order:
#       add_note(title, body)     body is optional
#       list_titles()             no arguments
#       find_notes(word)
#       delete_note(title)        must warn that it cannot be undone
#       calculate(expression)
#
# Argument names must match the functions in toolbox.py exactly.
