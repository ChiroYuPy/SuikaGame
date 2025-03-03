import yaml
from src.math.vector import Vector


class Config:
    WINDOW_WIDTH: int
    WINDOW_HEIGHT: int
    GRAVITY: Vector
    AIR_DENSITY: float
    FRUIT_MAX_SIZE: int
    MAX_GENERATION_SIZE: int
    FRUIT_DROP_COOLDOWN: float

    @classmethod
    def load_config(cls, config_file="config.yml"):
        with open(config_file, 'r') as file:
            cls.config = yaml.safe_load(file)

        cls.load_values()

    @classmethod
    def load_values(cls):
        cls.WINDOW_WIDTH = cls.get('window.width', 540)
        cls.WINDOW_HEIGHT = cls.get('window.height', 960)
        cls.GRAVITY = Vector(cls.get('gravity.x', 0), cls.get('gravity.y', 1024))
        cls.AIR_DENSITY = cls.get('air_density', 1.225)
        cls.FRUIT_MAX_SIZE = cls.get('max_size', 9)
        cls.MAX_GENERATION_SIZE = cls.get('max_generation_size', 3)
        cls.FRUIT_DROP_COOLDOWN = cls.get('fruit_drop_cooldown', 0.5)

    @classmethod
    def get(cls, key, default=None):
        keys = key.split('.')
        value = cls.config
        for key in keys:
            value = value.get(key, {})
        return value if value else default


Config.load_config("config.yml")

