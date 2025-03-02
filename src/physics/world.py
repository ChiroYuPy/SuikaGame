from src.core.config import GRAVITY
from src.physics.data_structures import CollisionManifold, CollisionPair


class World:
    def __init__(self):
        self.balls = []
        self.aabb_collisions = []
        self.collisions = []

        self._callbacks = []

    def addFruit(self, ball):
        self.balls.append(ball)

    def on_collision(self, func):
        self._callbacks.append(func)
        return func

    def update(self, dt, iterations=1):
        sub_dt = dt / iterations
        for _ in range(iterations):
            self.step(sub_dt)

    def step(self, dt):
        for ball in self.balls:
            ball.apply_acceleration(GRAVITY)
            ball.step(dt)
        self.broad_phase()
        self.narrow_phase()
        for callback in self._callbacks:
            callback(self.collisions)

    def broad_phase(self):
        self.aabb_collisions.clear()
        for a in range(len(self.balls) - 1):
            for b in range(a + 1, len(self.balls)):
                self.aabb_collisions.append(CollisionPair(self.balls[a], self.balls[b]))

    def narrow_phase(self):
        self.collisions.clear()
        for pair in self.aabb_collisions:
            collision_manifold = self.isCollide(pair.a, pair.b)
            if collision_manifold is not None:
                self.collisions.append(collision_manifold)
                self.separate(collision_manifold)
                self.resolve_collision(collision_manifold)

    @staticmethod
    def isCollide(a, b):
        radius_sum = a.radius + b.radius
        position_delta = (b.position - a.position)
        distance = position_delta.length()

        if distance >= radius_sum:
            return None

        normal = position_delta.normalize()
        depth = radius_sum - distance
        return CollisionManifold(a, b, normal, depth)

    @staticmethod
    def separate(collision_manifold):
        normal_dot_depth = collision_manifold.normal * collision_manifold.depth

        if not collision_manifold.b.activated:
            collision_manifold.a.position -= normal_dot_depth

        elif not collision_manifold.a.activated:
            collision_manifold.b.position += normal_dot_depth

        else:
            collision_manifold.a.position -= normal_dot_depth / 2
            collision_manifold.b.position += normal_dot_depth / 2

    @staticmethod
    def resolve_collision(collision_manifold):
        relative_velocity = collision_manifold.b.velocity - collision_manifold.a.velocity

        if relative_velocity.dot(collision_manifold.normal) > 0.0:
            return

        e = min(collision_manifold.a.restitution, collision_manifold.b.restitution)
        j = - (1.0 + e) * relative_velocity.dot(collision_manifold.normal)
        j = j / (collision_manifold.a.inv_mass + collision_manifold.b.inv_mass)

        impulse = j * collision_manifold.normal

        collision_manifold.a.velocity -= impulse * collision_manifold.a.inv_mass
        collision_manifold.b.velocity += impulse * collision_manifold.b.inv_mass