import time
import pygame
from pygame import Surface

from src.suika_game.config import Config
from src.physics.world import World


class PlayBox(World):
    def __init__(self, game, limit):
        super().__init__(gravity=Config.GRAVITY, air_density=Config.AIR_DENSITY)
        self.game = game
        self.limit = limit
        self.max_time_above_limit = 0
        self.death_advance = 0

    def step(self, dt):
        super().step(dt)
        self.contain_fruits()

    def contain_fruits(self):
        for fruit in self.balls:
            if fruit.x < fruit.radius:
                fruit.x = fruit.radius
                fruit.velocity.x *= -fruit.restitution

            elif fruit.x > self.game.display.get_width() - fruit.radius:
                fruit.x = self.game.display.get_width() - fruit.radius
                fruit.velocity.x *= -fruit.restitution

            if fruit.y < self.limit - fruit.radius:
                if fruit.activated and not hasattr(fruit, "death_time"):
                    fruit.death_time = time.time()

                if fruit.activated:
                    time_above_limit = time.time() - fruit.death_time
                    self.max_time_above_limit = max(self.max_time_above_limit, time_above_limit)
                    if time_above_limit > 3:
                        self.game.dead = True
                else:
                    if hasattr(fruit, "death_time"):
                        del fruit.death_time

            else:
                if hasattr(fruit, "death_time"):
                    del fruit.death_time

            if fruit.y > self.game.display.get_height() - fruit.radius:
                fruit.y = self.game.display.get_height() - fruit.radius
                fruit.velocity.y *= -fruit.restitution


    def draw(self, display):
        self.death_advance = min(self.max_time_above_limit / 3, 1.0)
        pygame.draw.line(display, (127, 127, 127), (0, self.limit), (display.get_width(), self.limit), 4)

        surface = Surface((display.get_width(), display.get_height())).convert_alpha()
        surface.fill((255, 0, 0, max(-64 + 64 * (self.death_advance*2), 0)))
        display.blit(surface, (0, 0))
