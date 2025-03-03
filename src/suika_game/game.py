import random
import time

import pygame

from src.suika_game.config import Config
from src.suika_game.floating_text import FloatingText
from src.suika_game.fruit import Fruit
from src.suika_game.hand import Hand
from src.suika_game.playbox import PlayBox
from src.math.functions import fibonacci
from src.math.vector import Vector
from src.ui.label import Label


class Game:
    def __init__(self):
        self.running = True
        pygame.display.set_mode((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
        pygame.display.set_caption("Fruit Game")
        self.display = pygame.display.get_surface()

        self.font96 = pygame.font.Font(None, 96)
        self.font64 = pygame.font.Font(None, 96)

        self.current_time = time.time()
        self.last_drop_time = self.current_time

        self.score = 0
        self.floating_score_texts = []


        self.dead = False

        self.game_over_label = Label("Game Over!", self.font64)
        self.game_over_label.set_position((Config.WINDOW_WIDTH / 2, Config.WINDOW_HEIGHT / 2))

        self.playbox = PlayBox(self, limit=256)
        self.hand = Hand(Vector(0, 128), Vector(self.display.get_width(), 128))
        self.handled_fruit = self.generate_fruit()

        self.key_pressed = set()

        self.playbox.on_collision(self.merge_fruits_on_collision)

    def generate_fruit(self):
        position = self.hand.get_cursor_position()
        fruit = Fruit(position.x, position.y, random.randint(1, Config.MAX_GENERATION_SIZE))
        fruit.activated = False
        self.playbox.addFruit(fruit)
        self.hand.start.x = fruit.radius
        self.hand.end.x = self.display.get_width() - fruit.radius
        return fruit

    def merge_fruits_on_collision(self, collisions):
        fruits_to_delete = set()
        for collision in collisions:
            if collision.a.activated and collision.b.activated and collision.a.size == collision.b.size:
                new_size = collision.a.size + 1
                new_position = (collision.a.position + collision.b.position) * 0.5
                fruits_to_delete.add(collision.a)
                fruits_to_delete.add(collision.b)
                self.score += fibonacci(new_size)

                popup = FloatingText(text=f"+{fibonacci(new_size)}", x=new_position.x, y=new_position.y, color=(0, 255, 0))
                self.floating_score_texts.append(popup)

                if new_size <= Config.FRUIT_MAX_SIZE:
                    self.playbox.addFruit(Fruit(new_position.x, new_position.y, new_size))

        for fruit in fruits_to_delete:
            self.playbox.balls.remove(fruit)

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.render()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.key_pressed.add(event.key)
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.KEYUP:
                if event.key in self.key_pressed:
                    self.key_pressed.remove(event.key)
                if event.key == pygame.K_SPACE:
                    if self.handled_fruit:
                        self.last_drop_time = self.current_time
                        self.handled_fruit.activated = True
                        self.handled_fruit = None

    def update(self):
        last_time = self.current_time
        self.current_time = time.time()
        dt = self.current_time - last_time
        if not self.dead:
            self.playbox.update(dt, iterations=4)

            if self.handled_fruit:
                self.handled_fruit.position = self.hand.get_cursor_position()
            elif self.current_time > self.last_drop_time + Config.FRUIT_DROP_COOLDOWN:
                self.handled_fruit = self.generate_fruit()

            if self.handled_fruit:
                if pygame.K_RIGHT in self.key_pressed:
                    self.hand.cursor += dt
                elif pygame.K_LEFT in self.key_pressed:
                    self.hand.cursor -= dt

            for floating_text in self.floating_score_texts:
                floating_text.update()

        self.floating_score_texts = [floating_text for floating_text in self.floating_score_texts if not floating_text.is_expired()]

    def render(self):
        self.display.fill((24, 24, 24))
        self.draw()
        pygame.display.flip()

    def draw(self):
        for ball in self.playbox.balls:
            ball.draw(self.display)

        for popup in self.floating_score_texts:
            popup.render(self.display)

        self.draw_uis(self.display)

    def draw_uis(self, display):
        self.playbox.draw(display)
        score_text = self.font96.render(f"{self.score}", True, (255, 255, 255))
        score_text_rect = score_text.get_rect()
        display.blit(score_text, ((display.get_width() - score_text_rect.width) / 2, 10))

        if self.dead:
            self.game_over_label.draw(display, center=True)