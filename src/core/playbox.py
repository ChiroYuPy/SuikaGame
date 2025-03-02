from src.physics.world import World


class PlayBox(World):
    def __init__(self, game):
        super().__init__()
        self.game = game
        
    def step(self, dt):
        super().step(dt)
        self.contain_fruits()
    
    def contain_fruits(self):
        for fruit in self.balls:
            if fruit.x < fruit.radius:
                fruit.x = fruit.radius
                fruit.velocity.x *= -fruit.restitution
            elif fruit.x > self.game.display.get_width() - fruit.radius:
                fruit.x = self.game.display.get_width() - fruit.radius
                fruit.velocity.x *= -fruit.restitution
            if fruit.y > self.game.display.get_height() - fruit.radius:
                fruit.y = self.game.display.get_height() - fruit.radius
                fruit.velocity.y *= -fruit.restitution