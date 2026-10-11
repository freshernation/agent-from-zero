# count_user(history) should return how many messages have the role "user".
def count_user(history):
    count = 0
    for message in history:
        if message["role"] == "User":
            count = count + 1
    return count
