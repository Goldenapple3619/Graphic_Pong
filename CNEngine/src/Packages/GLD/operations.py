def bool_(value, *args):
    if value == "true":
        return True

    elif value == "false":
        return False

    else:
        return True if value else False

def int_(value, *args):
    return int(value[0])

def float_(value, *args):
    return float(value[0])

def string_(value, *args):
    if type(value) == list and len(value) == 1 and isinstance(value[0], str):
        return str(value[0])
    else:
        return ''.join(str(c) for c in list(map(args[1], value)))