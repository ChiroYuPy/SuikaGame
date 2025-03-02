import pygame

from src.vector import Vector


class Hand:
    def __init__(self, start: Vector, end: Vector):
        self.start = start
        self.end = end
        self._cursor = 0.5

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, cursor):
        self._cursor = min(max(cursor, 0), 1)

    def set_cursor(self, cursor: float):
        self._cursor = cursor

    def get_cursor_position(self):
        return self.start + (self.end - self.start) * self.cursor

    def draw(self, display):
        pygame.draw.line(display, (255, 0, 0), self.start.toTuple(), self.end.toTuple(), 4)
        pygame.draw.circle(display, (0, 255, 0), self.get_cursor_position().toTuple(), 16)
