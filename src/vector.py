import math


class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, scalar: float):
        return self.__mul__(scalar)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def normalize(self):
        length = self.length()
        if length == 0.0:
            return Vector()
        return Vector(self.x / length, self.y / length)

    def toTuple(self):
        return self.x, self.y

    def zero(self):
        self.x = 0.0
        self.y = 0.0

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def rotate(self, angle):
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)
        return Vector(
            self.x * cos_theta - self.y * sin_theta,
            self.x * sin_theta + self.y * cos_theta
        )

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __str__(self):
        return f"Vector({self.x}, {self.y})"


