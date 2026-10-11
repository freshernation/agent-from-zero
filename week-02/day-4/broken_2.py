# first_words(history) should return a list holding the first word of every
# message:  ["Remember", "Saved."]
def first_words(history):
    words = []
    for message in history:
        words.append(message["text"].split()[0])
    return words
