# contents(history) should return the content of EVERY message, as a list.
def contents(history):
    result = []
    for message in history:
        result.append(message["content"])
        return result
