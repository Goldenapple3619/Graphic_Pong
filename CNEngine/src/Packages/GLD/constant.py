from .Exceptions import *
from .operations import *
from .commons import *

CLASSICS_OPERATORS = {
    "int": int_,
    "string": string_,
    "bool": bool_,
    "float": float_,
    "+": lambda *args: "+",
    "-": lambda *args: "-",
    "/": lambda *args: "/",
    "*": lambda *args: "*"
}

TAGS = {}

ERRORS = {
    1: GLDError("tag list not inited", "InitError", 1),
    100: GLDError("you forgot a bracket", "SyntaxError", 100),
    101: GLDError("you put a bracket at wrong place", "SyntaxError", 101),
    102: GLDError("You used an unreconized Tag $tag$", "TagError", 102),
    103: GLDError("You Forgot a semilicon", "SynaxError", 103)

}