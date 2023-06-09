from .check import *
from .libs import *


def reader(file_path: str, read_bytes: bool = False) -> str | bytes:
    checker(file_check, [file_path])
    ptr: TextIOWrapper = open(file_path, 'r') if not read_bytes else open(file_path, 'rb')
    value_str: str = ptr.read()
    ptr.close()

    return value_str

def write(file_path: str, content: str, write_bytes: bool = False, append: bool = False) -> None:
    checker(file_check, [file_path])
    if append: ptr: TextIOWrapper = open(file_path, 'w') if not write_bytes else open(file_path, 'wb')
    else: ptr: TextIOWrapper = open(file_path, 'a') if not write_bytes else open(file_path, 'ab')

    ptr.write(content)
    ptr.close()