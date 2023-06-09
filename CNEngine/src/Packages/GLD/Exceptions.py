class FileNotFound(Exception):
    def __init__(self: object, file: str) -> None:
        self.message = file + ' Does not exist'

class FolderNotFound(Exception):
    def __init__(self: object, folder: str) -> None:
        self.message = folder + ' Does not exist'

class GLDError:
    def __init__(self: object, message: str, name: str, code: str) -> None:
        self.name = name
        self.message = message
        self.code = code

    def copy(self) -> object:
        return GLDError(self.message, self.name, self.code)

    def __repr__(self: object) -> str:
        return f"ERR {self.code}: {self.name}, {self.message}, line: {self.line}"

    def launch(self: object, line: str) -> None:
        self.line = line
        print(self)
        exit(self.code)