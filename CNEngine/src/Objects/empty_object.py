class EmptyObject:
    def __init__(self: object, x: int, y: int, z:int = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

        self.draw_x = x
        self.draw_y = y

        self.draw_size_x = x
        self.draw_size_y = y

        self.components = []

    def add_component(self, component):
        self.components.append(component(self))

    def event(self, event):
        for component in self.components:
            component.event(event)

    def update(self: object, parent: object) -> None:
        for component in self.components:
            component.update(parent)

    def draw(self: object, *args: list) -> None:
        pass