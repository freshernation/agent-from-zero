# Day 3 - a conversation is a list of dictionaries.
#
#   make_message(role, content)           {"role": role, "content": content}
#   add_message(history, role, content)   appends to history; returns its new length
#   count_by_role(history)                {"user": 2, "assistant": 1};  {} when empty
#   last_from(history, role)              content of the latest message with that
#                                         role, or None
#   transcript(history)                   "user: hi\nassistant: hello";  "" when empty
