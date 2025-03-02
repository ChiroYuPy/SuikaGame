from src.math.functions import linear_progression
from src.math.vector import Vector


class VectorCursor:
    def __init__(self, start: Vector, end: Vector, progression_function=None):
        self.start = start
        self.end = end
        self._cursor = 0
        self.progression_function = progression_function if progression_function is not None else linear_progression

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, cursor):
        self._cursor = min(max(cursor, 0), 1)

    def set_cursor(self, cursor: float):
        self._cursor = cursor

    def get_cursor_position(self):
        return self.start + (self.end - self.start) * self.progression_function(self._cursor)

    def project_point_perpendicular(self, point: Vector):
        direction = self.end - self.start
        point_direction = point - self.start

        dot_product = point_direction.dot(direction)
        direction_length_squared = direction.length_squared()

        projection = self.start + (dot_product / direction_length_squared) * direction

        cursor_value = (projection - self.start).length() / direction.length()
        return projection, cursor_value

