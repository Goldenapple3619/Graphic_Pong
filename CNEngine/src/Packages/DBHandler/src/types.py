from .libs import *


@dataclass
class String:
    value: str
    size: int = 1
    max_size: int = 8000
    m_typ: str = "string"


@dataclass
class Char:
    value: str
    size: int = 1
    max_size: int = 1
    m_typ: str = "char"


@dataclass
class Float:
    value: float
    size: int = 256
    max_size: int = -1
    m_typ: str = "float"


@dataclass
class Int:
    value: int
    size: int = 256
    max_size: int = -1
    m_typ: str = "int"


@dataclass
class Bool:
    value: bool
    size: int = 1
    max_size: int = 1
    m_typ: str = "bool"


types = {
    "string": String,
    "char": Char,
    "float": Float,
    "int": Int,
    "bool": Bool
}