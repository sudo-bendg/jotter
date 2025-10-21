def validateInput(input):
    trimmedInput = input.strip()
    if not trimmedInput:
        return False
    if trimmedInput[0] == ' ':
        return False
    return trimmedInput