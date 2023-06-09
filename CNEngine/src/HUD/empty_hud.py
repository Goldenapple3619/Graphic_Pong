class EmptyHud:
    def __init__(self: object, x: int, y: int) -> None:
        self.x, self.y = x, y
        self.draw_x, self.draw_y = x, y

    def move(self, x, y):
        self.draw_x, self.draw_y = x, y

    def event(self, event):
        pass

    def update(self, parent):
        pass

    def draw(self, screen):
        pass