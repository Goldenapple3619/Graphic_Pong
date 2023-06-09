from .Exceptions import *
from .libs import *

def checker(check: object, args: list) -> None:
    check_ = check(*args)
    if check_[0]: raise(check_[1])

def file_check(file_path: str) -> tuple[bool, Exception]:
    if not isfile(file_path):
        return True, FileNotFound(file_path)
    else:
        False, None

def dir_check(folder_path: str) -> tuple[bool, Exception]:
    if not isdir(folder_path):
        return True, FolderNotFound(folder_path)
    else:
        False, None