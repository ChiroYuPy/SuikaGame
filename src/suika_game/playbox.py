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
        self.max_time_above_limit = 0  # Variable to track the maximum time a fruit stays above the limit
        self.death_advance = 0  # Factor that goes from 0 to 1

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
                if fruit.activated:
                    if not hasattr(fruit, "death_time"):  # Initialize death_time
                        fruit.death_time = time.time()  # Record current time
                    elif time.time() - fruit.death_time > 3:  # If more than 3 seconds passed
                        self.game.dead = True
                else:
                    if hasattr(fruit, "death_time"):  # Reset if the fruit is not activated
                        del fruit.death_time

                # Track the time above the limit for calculating death_advance
                if hasattr(fruit, "death_time"):
                    time_above_limit = time.time() - fruit.death_time
                    self.max_time_above_limit = max(self.max_time_above_limit, time_above_limit)

            else:
                if hasattr(fruit, "death_time"):  # Reset time if the fruit is no longer above the limit
                    del fruit.death_time

            if fruit.y > self.game.display.get_height() - fruit.radius:
                fruit.y = self.game.display.get_height() - fruit.radius
                fruit.velocity.y *= -fruit.restitution

        # Calculate death_advance as a value between 0 and 1 based on the time above the limit
        self.death_advance = min(self.max_time_above_limit / 3,
                                 1.0)  # Adjust the 10.0 divisor based on the game speed or limit

    def draw(self, display):
        # Draw the line that represents the limit
        pygame.draw.line(display, (127, 127, 127), (0, self.limit), (display.get_width(), self.limit), 4)

        # Draw the death_advance overlay on the screen
        surface = Surface((display.get_width(), display.get_height())).convert_alpha()
        surface.fill((255, 0, 0, 64 * self.death_advance))  # Apply the death_advance factor to the transparency
        display.blit(surface, (0, 0))
