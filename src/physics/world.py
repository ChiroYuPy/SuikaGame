import math

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
            self.apply_air_friction(ball)
            ball.step(dt)

    def apply_gravity_force(self, ball):
        ball.apply_acceleration(self.gravity)

    def apply_air_friction(self, ball):
        velocity_magnitude = ball.velocity.length()
        if velocity_magnitude > 0:
            drag_coefficient = ball.drag_coefficient
            area = math.pi * (ball.radius ** 2)
            drag_force_magnitude = 0.5 * drag_coefficient * self.air_density * area * (velocity_magnitude ** 2)

            # Direction opposée à la vitesse
            drag_force = ball.velocity.normalize() * -drag_force_magnitude
            ball.apply_force(drag_force)

    @staticmethod
    def generate_combinations(elements):
        num_elements = len(elements)
        for i in range(num_elements - 1):
            for j in range(i + 1, num_elements):
                yield elements[i], elements[j]

    def broad_phase(self):
        self.aabb_collisions.clear()
        for a in range(len(self.balls) - 1):
            for b in range(a + 1, len(self.balls)):
                self.aabb_collisions.append(CollisionPair(self.balls[a], self.balls[b]))

    def narrow_phase(self):
        self.collisions.clear()
        for pair in self.aabb_collisions:
            collision_manifold = Collisionner.isCollide(pair.a, pair.b)
            if collision_manifold is not None:
                self.collisions.append(collision_manifold)
                Resolver.separate(collision_manifold)
                Resolver.resolve_collision(collision_manifold)