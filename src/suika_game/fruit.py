import math

import pygame

from src.math.vector import Vector
from src.physics.ball import Ball
from src.suika_game.config import Config


class Fruit(Ball):
    def __init__(self, x, y, size):
        super().__init__(x=x, y=y, radius=size * 16 + 12, mass=size * 8 + 12, restitution=0)
        self.size = size

    def step(self, dt):
        super().step(dt)
        self.velocity -= self.velocity * dt

    def draw(self, display):
        green = max(min(self.size / Config.FRUIT_MAX_SIZE, 1), 0)
        red = 1 - green
        color = (red * 255, green * 255, 0)

        pygame.draw.circle(display, color, self.position.toTuple(), self.radius)
        cos = math.cos(math.radians(self.angle))
        sin = math.sin(math.radians(self.angle))
        angle_to_position = Vector(cos, sin) * self.radius
        pygame.draw.line(display, (255, 255, 255), self.position.toTuple(), (self.position + angle_to_position).toTuple())