import pygame

from src.core.game import Game


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()