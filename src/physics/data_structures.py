import dataclasses

from src.core.fruit import Fruit
from src.math.vector import Vector


@dataclasses.dataclass
class CollisionPair:
    a: Fruit
    b: Fruit


@dataclasses.dataclass
class CollisionManifold:
    a: Fruit
    b: Fruit
    normal: Vector
    depth: float
