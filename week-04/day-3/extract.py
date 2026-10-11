# Day 3 - structured output you do not trust blindly.
#
#   parse_json(text)     the dict inside the text, or None.
#                        Must cope with JSON wrapped in prose or a code fence.
#   is_note(data)        True if data is a dict with a non-empty string "title"
#                        and a string "body"
#   extract_note(model, sentence)
#                        a valid note dict, or None. One call if the first
#                        answer is valid; otherwise ONE retry in the same
#                        conversation, telling the model what was wrong.
