from .empty_component import EmptyComponent

class Script(EmptyComponent):
    def __init__(self, parent):
        super().__init__(parent)

    def event(self):
        pass

    def update(self):
        pass