import time
import pygame.draw

from src.suika_game.config import Config
from src.physics.world import World


class PlayBox(World):
    def __init__(self, game, limit):
        super().__init__(gravity=Config.GRAVITY, air_density=Config.AIR_DENSITY)
        self.game = game
        self.limit = limit

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

            if fruit.y < self.limit + fruit.radius:
                if getattr(fruit, "activated", False):  # Vérifie si le fruit est activé
                    if not hasattr(fruit, "death_time"):  # Initialisation de death_time
                        fruit.death_time = time.time()  # Enregistrer le temps actuel
                    elif time.time() - fruit.death_time > 3:  # Si plus de 3 secondes sont passées
                        fruit.death = True  # Marquer le fruit comme "mort"
                        self.game.running = False
                else:
                    if hasattr(fruit, "death_time"):  # Réinitialiser si le fruit n'est pas activé
                        del fruit.death_time

            else:
                if hasattr(fruit, "death_time"):  # Réinitialiser le temps si le fruit ne dépasse plus la limite
                    del fruit.death_time
                if hasattr(fruit, "death"):  # Réinitialiser la variable death si elle existe
                    del fruit.death

            if fruit.y > self.game.display.get_height() - fruit.radius:
                fruit.y = self.game.display.get_height() - fruit.radius
                fruit.velocity.y *= -fruit.restitution

    def draw(self, display):
        pygame.draw.line(display, (127, 127, 127), (0, self.limit), (display.get_width(), self.limit), 4)
