# with_message(history, message) should return a NEW list: everything in
# history, plus message on the end. The history passed in must not change.
def with_message(history, message):
    extended = history
    extended.append(message)
    return extended
