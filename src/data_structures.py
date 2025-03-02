import dataclasses

from src.fruit import Fruit
from src.vector import Vector


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
