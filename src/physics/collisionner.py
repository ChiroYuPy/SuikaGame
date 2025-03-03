from src.physics.data_structures import CollisionManifold


class Collisionner:
    @staticmethod
    def isCollide(a, b):
        radius_sum = a.radius + b.radius
        position_delta = (b.position - a.position)
        distance = position_delta.length()

        if distance >= radius_sum:
            return None

        normal = position_delta.normalize()
        depth = radius_sum - distance

        contact_point = a.position + normal * b.radius

        return CollisionManifold(a, b, normal, depth, contact_point)