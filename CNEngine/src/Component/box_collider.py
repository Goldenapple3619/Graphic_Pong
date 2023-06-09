from .empty_component import EmptyComponent
from ..libs import draw, display

class BoxCollider(EmptyComponent):
    def __init__(self, parent, x=0, y=0, end_x=0, end_y=0):
        super().__init__(parent)

        self.x = parent.draw_x + x
        self.y = parent.draw_y + y


        self.end_x = (parent.size_x + end_x) * parent.pixel_size
        self.end_y = (parent.size_y + end_y) * parent.pixel_size

        self.create_collid_segment()

        self.collid_vectors = [(0,0) for _ in self.collid_segments]

        self.create_movement_vectors(self.x,self.y)

        self.create_collid_zone()

    def create_movement_vectors(self, next_x, next_y):
        collid_segments = self.collid_segments

        for i, item in enumerate(collid_segments):

            actual_x, actual_y = collid_segments[item]

            self.collid_vectors[i] = (next_x - actual_x, next_y - actual_y, next_x, next_y, actual_x, actual_y)

        self.parent.collid_vectors = self.collid_vectors

    def check_collid(self, parent):
        collid_vectors = self.collid_vectors
        for item in parent.objects:
            if not hasattr(item, "collid_zones") and id(item) != id(self):
                continue

            for vector in collid_vectors:
                for lines in item.collid_zones:
                    try:
                        result = (vector[1]/vector[0])-((lines[1][1]-lines[0][1])/(lines[1][0]-lines[0][0]))
                    except ZeroDivisionError:
                        result = 0

                    if result != 0:
                        Xa, Xb = vector[4], vector[2]
                        Ya, Yb = vector[5], vector[3]

                        Xc, Xd = lines[0][0],lines[1][0]
                        Yc, Yd = lines[0][1],lines[1][1]

                        part_0 = ((Yb-Ya)/(Xb-Xa))
                        part_1 = ((lines[1][1]-lines[0][1])/(lines[1][0]-lines[0][0]))

                        Xi=(part_0*Xa+Ya-part_1*Xc-Yc) / (part_0-part_1)
                        Yi=(part_0*((part_0*Xa+Ya-part_1*Xc-Yc)) / (part_0-part_1)-Xa)+Ya


                        if (Xb > Xi and Xa < Xi) and (Yb > Yi and Yi > Ya) :
                            self.parent.move(Xi-self.parent.draw_size_x, Yi-self.parent.draw_size_y, self.parent.z)
                            parent.camera.move(Xi-self.parent.draw_size_x, Yi-self.parent.draw_size_y, parent.camera.z)


    def create_collid_segment(self):
        self.collid_segments = {
            "top_left": (self.x,self.y),
            "down_right": (self.end_x + self.x, self.end_y + self.y),
            "top_right": (self.end_x + self.x, self.y),
            "down_left": (self.x, self.y + self.end_y)
        }

        self.parent.collid_segments = self.collid_segments

    def create_collid_zone(self):
        segs = self.collid_segments
        self.collid_zones = [(segs["top_left"], segs["top_right"]), (segs["top_left"], segs["down_left"]), (segs["top_right"], segs["down_right"]), (segs["down_left"], segs["down_right"])]
        self.parent.collid_zones = self.collid_zones

    def update(self: object, parent: object):
        if self.parent.draw_x != self.x or self.parent.draw_y != self.y:

            self.create_movement_vectors(self.parent.draw_x, self.parent.draw_y)

            self.x, self.y = self.parent.draw_x, self.parent.draw_y

            self.create_collid_segment()

            self.create_collid_zone()

        self.check_collid(parent)


        super().update(parent)