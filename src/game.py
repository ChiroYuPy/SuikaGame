import random
import time

import pygame

from src.config import FRUIT_DROP_COOLDOWN, MAX_SIZE, MAX_GENERATION_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from src.fruit import Fruit
from src.hand import Hand
from src.vector import Vector
from src.world import World


class Game:
    def __init__(self):
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Fruit Game")
        self.display = pygame.display.get_surface()
        self.running = True
        self.current_time = time.time()
        self.last_drop_time = self.current_time

        self.world = World()

        self.hand = Hand(Vector(0, 32), Vector(self.display.get_width(), 32))
        self.handled_fruit = self.generate_fruit()

        self.key_pressed = set()

        self.world.on_collision(self.merge_fruits_on_collision)

    def generate_fruit(self):
        position = self.hand.get_cursor_position()
        fruit = Fruit(position.x, position.y, random.randint(1, MAX_GENERATION_SIZE))
        fruit.activated = False
        self.world.addFruit(fruit)
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
                if new_size <= MAX_SIZE:
                    self.world.addFruit(Fruit(new_position.x, new_position.y, new_size))

        for fruit in fruits_to_delete:
            self.world.balls.remove(fruit)

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
        self.world.step(dt, iterations=4)
        self.contain_fruits()

        if self.handled_fruit:
            self.handled_fruit.position = self.hand.get_cursor_position()
        elif self.current_time > self.last_drop_time + FRUIT_DROP_COOLDOWN:
            self.handled_fruit = self.generate_fruit()

        if self.handled_fruit:
            if pygame.K_RIGHT in self.key_pressed:
                self.hand.cursor += dt
            elif pygame.K_LEFT in self.key_pressed:
                self.hand.cursor -= dt

    def contain_fruits(self):
        for fruit in self.world.balls:
            if fruit.x < fruit.radius:
                fruit.x = fruit.radius
                fruit.velocity.x *= -fruit.restitution
            elif fruit.x > self.display.get_width() - fruit.radius:
                fruit.x = self.display.get_width() - fruit.radius
                fruit.velocity.x *= -fruit.restitution
            if fruit.y > self.display.get_height() - fruit.radius:
                fruit.y = self.display.get_height() - fruit.radius
                fruit.velocity.y *= -fruit.restitution

    def render(self):
        self.display.fill((24, 24, 24))
        self.draw()
        pygame.display.flip()

    def draw(self):
        for ball in self.world.balls:
            ball.draw(self.display)