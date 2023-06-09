from .HUD import *
from .Objects import *
from .Preset import *
from .Component import *
from .commons import *

MEM = ["NULL" for _ in range(30)]
CUSTOM_CLASS = {}

def _attrs_eval(obj, attrs):
    at, value = attrs[1]
    command = attrs[0]

    if command == "set":
        setattr(obj, at, value)

    elif command == "append":
        getattr(obj, at).append(value)

    elif command == "callattr":
        if not isinstance(value, list) or not isinstance(value, tuple):
            getattr(obj, at)(value)
        else:
            getattr(obj, at)(*value)


def _attrs_operations(content, interpreteur):
    at = None
    obj = None

    for item in list(map(interpreteur, content)):
        if item[0] == "at":
            at = item[1]

        elif item[0] == "content":
            obj = item[1]

    return (at, obj)

def using_(content, game, interpreteur):
    pass

def class_(content, game, interpreteur):
    inner_tags = {key: value for key, value in list(map(interpreteur, content))}

    if "call" in inner_tags and inner_tags["call"] != None:
        call = inner_tags["call"]
    else:
        return None

    if "args" in inner_tags:
        C = call(*inner_tags["args"])

    else:
        C = call()

    if "attrs" in inner_tags:
        for item in inner_tags["attrs"]:
            _attrs_eval(C, item)

    return C

def hud_(content, game, interpreteur):
    content = list(map(interpreteur, content))[0]
    game.add_hud(content)


def object_(content, game, interpreteur):
    content = list(map(interpreteur, content))[0]
    game.add_object(content)

def function_call_(content, game, interpreteur):
    inner_tags = {key: value for key, value in list(map(interpreteur, content))}

    if "call" in inner_tags and inner_tags["call"] != None:
        call = inner_tags["call"]
    else:
        return None

    if "args" in inner_tags:
        C = call(*inner_tags["args"])

    else:
        C = call()

    return C

def mem_save_(content, game, interpreteur):
    at, content = _attrs_operations(content, interpreteur)

    MEM[interpreteur(at)] = content

def mem_load_(content, game, interpreteur):
    at = {key: value for key, value in list(map(interpreteur, content))}["at"]

    return MEM[interpreteur(at)]

def script_(content, game, interpreteur):
    inner_tags = {key: value for key, value in list(map(interpreteur, content))}

    return

    #if "call" in inner_tags and inner_tags["call"] != None:
    #    call = inner_tags["call"]
    #else:
    #    return None

    #if "args" in inner_tags:
    #    C = call(*inner_tags["args"])

    #else:
    #    C = call()

def args_(content, game, interpreteur):
    return ("args", list(map(interpreteur, content)))

def call_(content, game, interpreteur):
    content = content[0]

    try:
        return ("call", eval(content))
    except Exception:
        if content in CUSTOM_CLASS:
            return ("call", CUSTOM_CLASS[content])
        return ("call", None)

def attrs_(content, game, interpreteur):
    return ("attrs", list(map(interpreteur, content)))

def append_(content, game, interpreteur):
    return ("append", _attrs_operations(content, interpreteur))

def set_(content, game, interpreteur):
    return ("set",  _attrs_operations(content, interpreteur))

def callattr_(content, game, interpreteur):
    return ("callattr",  _attrs_operations(content, interpreteur))

def function_(content, game, interpreteur):
    return eval(content[0])

def at_(content, game, interpreteur):
    return ("at", content[0])

def content_(content, game, interpreteur):
    content = list(map(interpreteur, content))[0]

    return ("content", content)

def log_(content, game, interpreteur):
    print(*list(map(interpreteur, content)))

def math_(content, game, interpreteur):
    content = list(map(interpreteur, content))[0]
    return eval(content)

tag_pool = {
    "class": class_,
    "hud": hud_,
    "object": object_,
    "script": script_,
    "call": call_,
    "attrs": attrs_,
    "at": at_,
    "set": set_,
    "args": args_,
    "funcall": function_call_,
    "append": append_,
    "content": content_,
    "callattr": callattr_,
    "function": function_,
    "using": using_,
    "msave": mem_save_,
    "mload": mem_load_,
    "log": log_,
    "math": math_
}