from src.math.vector import Vector


class Label:
    def __init__(self, text, font):
        self.position = Vector(0, 0)
        self.font = font
        self.text = text

    def set_position(self, position):
        self.position = position

    def draw(self, display, center=False):
        text_render = self.font.render(self.text, True, (255, 255, 255))
        if center:
            display.blit(text_render, text_render.get_rect(center=self.position))
        else:
            display.blit(text_render, text_render.get_rect(top_left=self.position))