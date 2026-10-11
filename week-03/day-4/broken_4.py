# average_tool("2, 4") should return "3.0".
# It is a TOOL, so it must never raise: anything that is not a list of numbers
# should return "Error: not a number".
def average_tool(text):
    try:
        numbers = []
        for part in text.split(","):
            numbers.append(float(part))
        return str(sum(numbers) / len(numbers))
    except ZeroDivisionError:
        return "Error: not a number"
