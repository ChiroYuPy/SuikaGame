import yaml

from src.vector import Vector


class Config:
    def __init__(self, config_file="config.yml"):
        self.config = self.load_config(config_file)

    @staticmethod
    def load_config(config_file):
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)

    def get(self, key, default=None):
        """Retourne la valeur de la configuration pour une clé donnée."""
        keys = key.split('.')
        value = self.config
        for key in keys:
            value = value.get(key, {})
        return value if value else default


config = Config()


WINDOW_WIDTH = config.get("window.width", 540)
WINDOW_HEIGHT = config.get("window.height", 960)
GRAVITY = Vector(config.get('gravity.x', 0), config.get('gravity.y', 1024))
MAX_SIZE = config.get('max_size', 9)
MAX_GENERATION_SIZE = config.get('max_generation_size', 3)
FRUIT_DROP_COOLDOWN = config.get('fruit_drop_cooldown', 0.5)