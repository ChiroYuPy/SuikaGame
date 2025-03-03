import math

import pygame

from src.math.functions import fibonacci
from src.math.vector import Vector
from src.physics.ball import Ball
from src.suika_game.config import MAX_SIZE


class Fruit(Ball):
    def __init__(self, x, y, size):
        super().__init__(x=x, y=y, radius=fibonacci(size+1) * 8 + 12, mass=size)
        self.size = size

    def draw(self, display):
        green = max(min(self.size / MAX_SIZE, 1), 0)
        red = 1 - green
        color = (red * 255, green * 255, 0)

        pygame.draw.circle(display, color, self.position.toTuple(), self.radius)
        cos = math.cos(math.radians(self.angle))
        sin = math.sin(math.radians(self.angle))
        angle_to_position = Vector(cos, sin) * self.radius
        pygame.draw.line(display, (255, 255, 255), self.position.toTuple(), (self.position + angle_to_position).toTuple())