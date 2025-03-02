import time
import pygame

from src.math.vector import Vector


class FloatingText:
    def __init__(self, text, x, y, duration=1, color=(255, 255, 255)):
        self.text = text
        self.position = Vector(x, y)
        self.duration = duration
        self.start_time = time.time()
        self.alpha = 255
        self.font = pygame.font.Font(None, 64)
        self.color = color

    def update(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time < self.duration:
            self.alpha = min(255, int(255 * (1 - elapsed_time / self.duration)))
        else:
            self.alpha = 255

    def render(self, display):
        text_surface = self.font.render(self.text, True, self.color)
        text_surface.set_alpha(self.alpha)
        text_rect = text_surface.get_rect()
        display.blit(text_surface, (self.position.x - text_rect.width / 2, self.position.y - text_rect.height / 2))

    def is_expired(self):
        return time.time() - self.start_time > self.duration
