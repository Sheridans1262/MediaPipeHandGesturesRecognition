import enum


class Finger(enum.IntEnum):
    thumb = 0,
    index = 1,
    middle = 2,
    ring = 3,
    pinky = 4


class Dot:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"x={self.x} y={self.y} z={self.z}"
