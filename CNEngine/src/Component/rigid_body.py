from .empty_component import EmptyComponent

class RigidBody(EmptyComponent):
    def __init__(self, parent, mass=1.5, gravity=9.80665):
        super().__init__(parent)

        self.mass = mass
        self.gravity = gravity
        self.force = 0

        self.calc_weight()

    def calc_weight(self):
        self.weight = self.mass * self.gravity

    def reset_force(self):
        self.force = 0

    def update(self: object, parent: object):
        if self.force < self.gravity*2:
            self.force += 0.3
        self.parent.move(self.parent.x, self.parent.y+((1/2)*(self.weight+self.force)*(parent.clock.get_fps()/60)**2), self.parent.z)