class FileNotFound(Exception):
    def __init__(self: object, file: str) -> None:
        self.message = file + ' Does not exist'

class FolderNotFound(Exception):
    def __init__(self: object, folder: str) -> None:
        self.message = folder + ' Does not exist'

class NoCameraSet(Exception):
    def __init__(self: object) -> None:
        self.message = "You forgot to put camera to game please do game.set_camera(your_camera)"

class GameNotInited(Exception):
    def __init__(self: object) -> None:
        self.message = "Game as not been inited"