import pygame
from pygame.locals import *


class Event():
    def __init__(self, game):
        self.game = game

    def listen(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                self.game.Run = False

            if event.type == MOUSEBUTTONDOWN and not self.game.gameover and not self.game.win:
                mouse = pygame.mouse.get_pressed()
                if mouse[0] == 1:
                    self.game.handler.leftmouseclicked(event.pos)
                elif mouse[2] == 1:
                    self.game.handler.rightmouseclicked(event.pos)
            if self.game.gameover or self.game.win:
                if event.type == KEYDOWN and event.key == K_r:
                    self.game.reset()

        if not self.game.win:
            self.game.win = self.game.handler.isWin()
