import math

from src.math.functions import generate_combinations
from src.math.vector import Vector
from src.physics.collisionner import Collisionner
from src.physics.data_structures import CollisionPair
from src.physics.resolver import Resolver


class World:
    def __init__(self, gravity=Vector(), air_density=Vector()):
        self.balls = []

        self.aabb_collisions = []
        self.collisions = []

        self.gravity = gravity
        self.air_density = air_density

        self._callback = None

    def addFruit(self, ball):
        self.balls.append(ball)

    def on_collision(self, func):
        self._callback = func
        return func

    def update(self, dt, iterations=1):
        sub_dt = dt / iterations
        for _ in range(iterations):
            self.step(sub_dt)
            if self._callback:
                self._callback(self.collisions)

    def step(self, dt):
        self.step_phase(dt)
        self.broad_phase()
        self.narrow_phase()

    def step_phase(self, dt):
        for ball in self.balls:
            self.apply_gravity_force(ball)
            ball.step(dt)

    def apply_gravity_force(self, ball):
        ball.apply_acceleration(self.gravity)

    def broad_phase(self):
        self.aabb_collisions.clear()
        self.aabb_collisions.extend(CollisionPair(ball_a, ball_b) for ball_a, ball_b in generate_combinations(self.balls))

    def narrow_phase(self):
        self.collisions.clear()
        for pair in self.aabb_collisions:
            collision_manifold = Collisionner.isCollide(pair.a, pair.b)
            if collision_manifold is not None:
                self.collisions.append(collision_manifold)
                Resolver.separate(collision_manifold)
                Resolver.resolve_collision(collision_manifold)