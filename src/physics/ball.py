from src.math.functions import get_moment_of_inertia
from src.math.vector import Vector


class Ball:
    def __init__(self, x, y, radius, mass=1, restitution=1, dynamic_friction=0.5, static_friction=0.5):
        self.position = Vector(x, y)
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)

        self.angle = 0
        self.angular_velocity = 0
        self.radius = radius

        self.mass = mass
        self.inv_mass = 1 / self.mass if self.mass > 0 else float('inf')

        self.inertia = get_moment_of_inertia("ball", self.mass, self.radius)
        self.inv_inertia = 1 / self.inertia if self.inertia > 0 else float('inf')

        self.restitution = restitution
        self.dynamic_friction = dynamic_friction
        self.static_friction = static_friction

        self.activated = True

    @property
    def x(self):
        return self.position.x

    @x.setter
    def x(self, value):
        self.position.x = value

    @property
    def y(self):
        return self.position.y

    @y.setter
    def y(self, value):
        self.position.y = value

    @property
    def vx(self):
        return self.velocity.x

    @vx.setter
    def vx(self, value):
        self.velocity.x = value

    @property
    def vy(self):
        return self.velocity.y

    @vy.setter
    def vy(self, value):
        self.velocity.y = value

    def step(self, dt):
        if self.activated:
            if self.mass > 0:
                self.velocity += self.acceleration * dt
            self.position += self.velocity * dt
            self.angle += self.angular_velocity * dt
        else:
            self.velocity *= 0
        self.acceleration *= 0

    def apply_acceleration(self, acceleration):
        self.acceleration += acceleration

    def apply_force(self, force: Vector):
        self.acceleration += force / self.mass

