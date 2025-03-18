from src.math.vector import Vector


class Resolver:
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

        impulse = collision_manifold.normal * j

        collision_manifold.a.velocity -= impulse * collision_manifold.a.inv_mass
        collision_manifold.b.velocity += impulse * collision_manifold.b.inv_mass

    # not yet used
    @staticmethod
    def resolve_collision_with_rotation_and_friction(collision_manifold):
        e = min(collision_manifold.a.restitution, collision_manifold.b.restitution)

        sf = (collision_manifold.a.static_friction + collision_manifold.b.static_friction) * 0.5
        df = (collision_manifold.a.dynamic_friction + collision_manifold.b.dynamic_friction) * 0.5

        ra = collision_manifold.contact_point - collision_manifold.a.position
        rb = collision_manifold.contact_point - collision_manifold.b.position

        ra_perp = Vector(-ra.y, ra.x)
        rb_perp = Vector(-rb.y, rb.x)

        angular_linear_velocity_a = ra_perp * collision_manifold.a.angular_velocity
        angular_linear_velocity_b = rb_perp * collision_manifold.b.angular_velocity

        relative_velocity = ((collision_manifold.b.velocity + angular_linear_velocity_b) -
                             (collision_manifold.a.velocity + angular_linear_velocity_a))

        relative_velocity_dot = relative_velocity.dot(collision_manifold.normal)

        if relative_velocity_dot > 0:
            return

        ra_perp_dot_n = ra_perp.dot(collision_manifold.normal)
        rb_perp_dot_n = rb_perp.dot(collision_manifold.normal)

        denominator = (collision_manifold.a.inv_mass + collision_manifold.b.inv_mass +
                       (ra_perp_dot_n + ra_perp_dot_n) * collision_manifold.a.inv_inertia +
                       (rb_perp_dot_n * rb_perp_dot_n) * collision_manifold.b.inv_inertia)

        j = - (1.0 + e) * relative_velocity_dot
        j /= denominator

        impulse = collision_manifold.normal * j

        collision_manifold.a.velocity -= impulse * collision_manifold.a.inv_mass
        collision_manifold.a.angular_velocity -= ra.cross(impulse) * collision_manifold.a.inv_inertia
        collision_manifold.b.velocity += impulse * collision_manifold.b.inv_mass
        collision_manifold.b.angular_velocity += rb.cross(impulse) * collision_manifold.b.inv_inertia



        tangent = relative_velocity - relative_velocity_dot * collision_manifold.normal

        if tangent.length_squared() < 1e-6:
            return
        else:
            tangent = tangent.normalize()

        ra_perp_dot_tangent = ra_perp.dot(tangent)
        rb_perp_dot_tangent = rb_perp.dot(tangent)

        denominator = (collision_manifold.a.inv_mass + collision_manifold.b.inv_mass +
                       (ra_perp_dot_tangent ** 2) * collision_manifold.a.inv_inertia +
                       (rb_perp_dot_tangent ** 2) * collision_manifold.b.inv_inertia)

        jt = -relative_velocity.dot(tangent)
        jt /= denominator

        if abs(jt) <= j * sf:
            friction_impulse = jt * tangent
        else:
            friction_impulse = -j * tangent * df

        collision_manifold.a.velocity -= friction_impulse * collision_manifold.a.inv_mass
        collision_manifold.a.angular_velocity -= ra.cross(friction_impulse) * collision_manifold.a.inv_inertia
        collision_manifold.b.velocity += friction_impulse * collision_manifold.b.inv_mass
        collision_manifold.b.angular_velocity += rb.cross(friction_impulse) * collision_manifold.b.inv_inertia