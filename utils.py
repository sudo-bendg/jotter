def validateInput(input, charset = None):
    trimmedInput = input.strip()
    if not trimmedInput:
        return False
    if trimmedInput[0] == ' ':
        return False
    if charset:
        for char in input:
            if not char in charset:
                return False
    return trimmedInput