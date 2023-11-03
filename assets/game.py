import pygame
import sys
from assets.window import Window
from assets.handler import Handler
from assets.event import Event


class Game(object):

    def __init__(self) -> None:
        self.window = Window(self)
        self.handler = Handler(self)
        self.event = Event(self)
        self.amountOfTick = 60
        self.Run = False
        self.gameover = False
        self.win = False

    def start(self):
        if not pygame.get_init():
            pygame.init()
            self.Run = True
        while self.Run:
            self.event.listen()
            if not self.Run:
                break
            self.window.DISPLAYSURF.fill((0, 0, 0))
            self.window.draw()
            self.window.update()
            pygame.time.Clock().tick(self.amountOfTick)
        self.stop()

    def reset(self):
        self.handler.reset()
        self.gameover = False
        self.win = False

    def stop(self):
        pygame.quit()
        sys.exit()
