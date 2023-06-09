from .check import *
from .libs import *
from .constants import *

def get_working_dir() -> str:
    return '/'.join(__file__.replace('\\', '/').split('/')[:-2])

def get_disk_usage() -> float:
    ic = Process(getpid()).io_counters()

    return round(ic.read_bytes / 1024 ** 2, 2), round(ic.write_bytes / 1024 ** 2, 2)

def get_cpu_percent() -> float:
    return Process(getpid()).cpu_percent(0)

def get_total_memory() -> float:
    return round(virtual_memory().total / 1024 ** 2, 2)

def get_memory_usage() -> float:
    return round(Process(getpid()).memory_info().rss / 1024 ** 2, 2)

def get_image(name: str) -> Surface:
    return LOADED_IMAGES[name].copy().convert_alpha()

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
