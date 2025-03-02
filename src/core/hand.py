import pygame

from src.math.functions import *
from src.math.vector import Vector
from src.math.vector_cursor import VectorCursor


class Hand(VectorCursor):
    def __init__(self, start: Vector, end: Vector):
        super().__init__(start, end, progression_function=ease_in_out_progression)
        self._cursor = 0.5

    def draw(self, display):
        pygame.draw.line(display, (255, 0, 0), self.start.toTuple(), self.end.toTuple(), 4)
        pygame.draw.circle(display, (0, 255, 0), self.get_cursor_position().toTuple(), 16)
