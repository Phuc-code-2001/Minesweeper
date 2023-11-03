import pygame
from assets.blinktext import BlinkText


class Window:
    def __init__(self, game) -> None:
        self.game = game
        self.WIDTH = 800
        self.HEIGHT = 600
        self.sizeBlock = 40
        self.numOfBlockWitdh = self.WIDTH // self.sizeBlock
        self.numOfBlockHeight = self.HEIGHT // self.sizeBlock
        self.DISPLAYSURF = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.congratulate = BlinkText(game, "YOU WIN, congratulations !!! R to Reset")
        self.overtext = BlinkText(game, "You Lost, R to Reset !!!")
        self.set_caption("Mineswapper")

    def set_caption(self, str):
        pygame.display.set_icon(pygame.image.load("icon_W70_icon.ico"))
        pygame.display.set_caption(str)

    def draw(self):
        self.game.handler.draw()

    def update(self):
        pygame.display.flip()
