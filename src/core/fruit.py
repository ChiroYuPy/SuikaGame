import pygame

from src.physics.ball import Ball
from src.core.config import MAX_SIZE


class Fruit(Ball):
    def __init__(self, x, y, size):
        super().__init__(x=x, y=y, radius=size*8+24, mass=size)
        self.size = size

    def draw(self, display):
        green = max(min(self.size / MAX_SIZE, 1), 0)
        red = 1 - green
        color = (red * 255, green * 255, 0)

        pygame.draw.circle(display, color, self.position.toTuple(), self.radius)