class Camera:
    def __init__(self: object, x: int, y: int, z: int = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def move(self: object, x: int, y: int, z: int = 0) -> None:
        self.x = x
        self.y = y
        self.z = z