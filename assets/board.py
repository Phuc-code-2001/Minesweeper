import numpy
import pygame
from assets.image import *


class Board:
    def __init__(self, game):
        self.game = game
        self.width = self.game.window.numOfBlockWitdh
        self.height = self.game.window.numOfBlockHeight
        self.sizeBlock = self.game.window.sizeBlock
        self.array = numpy.zeros((self.height, self.width), dtype=numpy.int8)
        self.statusArray = numpy.zeros(
            (self.height, self.width), dtype=numpy.bool)
        self.flags = numpy.zeros((self.height, self.width), dtype=numpy.bool)
        self.mapDraw = []
        self.maxNum = 4
        self.boomIdx = -1
        self.numOfBoom = int(self.width * self.height * 0.2)
        # self.numOfBoom = 1
        self.numOfClose = self.width * self.height
        self.directs = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                        (0, 1), (1, -1), (1, 0), (1, 1)]

    def floodFill(self, x, y):
        stack = [(x, y)]
        while len(stack) > 0:
            pixel = stack.pop(0)
            # print(pixel)
            for dx, dy in self.directs:
                _x = pixel[0] + dx
                _y = pixel[1] + dy
                # print(_x, _y)
                if (0 <= _x < self.width) and (0 <= _y < self.height) and self.statusArray[_y, _x] == 0:
                    if (self.array[_y, _x] == 0):
                        self.statusArray[_y, _x] = 1
                        self.numOfClose -= 1
                        stack.append((_x, _y))
                    else:
                        self.statusArray[_y, _x] = 1
                        self.numOfClose -= 1

        # print("Filled...")

    def countBoomAround(self, x, y):
        cnt = 0
        for dx, dy in self.directs:
            _x, _y = x + dx, y + dy
            if (0 <= _x < self.width) and (0 <= _y < self.height) and self.array[_y, _x] == -1:
                cnt += 1
                if cnt >= 4:
                    return cnt
        return cnt

    def _initializeBoom(self, ax, ay):
        import random
        cnt = 0
        while cnt < self.numOfBoom:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.array[y, x] != -1 and (abs(x - ax) > 1 or abs(y - ay) > 1):
                isSelected = 1
                for dx, dy in self.directs:
                    _x = x + dx
                    _y = y + dy
                    if (0 <= _x < self.width) and (0 <= _y < self.height) and (self.array[y, x] == 0) and self.countBoomAround(_x, _y) >= 4:
                        isSelected = 0
                        break
                if isSelected:
                    self.array[y, x] = -1
                    cnt += 1

    def _initializeMap(self):
        for y in range(self.height):
            row = []
            for x in range(self.width):
                surface = self.createSurfaceByIdx(self.array[y, x])
                row.append(surface)
            self.mapDraw.append(row)

    def draw(self):
        border = 1
        DISPLAYSURF = self.game.window.DISPLAYSURF
        for x in range(self.width):
            for y in range(self.height):
                _x = x * self.sizeBlock
                _y = y * self.sizeBlock
                if self.statusArray[y, x]:
                    DISPLAYSURF.blit(self.mapDraw[y][x], (_x, _y))
                else:
                    if self.flags[y, x]:
                        # pygame.draw.rect(
                        #     DISPLAYSURF, (255, 255, 0), (_x, _y, self.sizeBlock - border, self.sizeBlock - border))
                        DISPLAYSURF.blit(flag_img, (_x, _y))
                    else:
                        pygame.draw.rect(
                            DISPLAYSURF, (128, 128, 128), (_x, _y, self.sizeBlock - border, self.sizeBlock - border))

    def createSurfaceByIdx(self, idx):
        border = 1
        mainSurface = pygame.Surface(
            (self.sizeBlock - border, self.sizeBlock - border))
        mainSurface.fill((128, 50, 50))
        center = [(self.sizeBlock - border) // 2,
                  (self.sizeBlock - border) // 2]
        if idx == -1:
            mainSurface.blit(mine_img, (0, 0))
            # pygame.draw.circle(mainSurface, (0, 0, 0),
            #                    center, self.sizeBlock // 2)

        elif idx == 0:
            ...
        else:
            font = pygame.font.SysFont('concolas', self.sizeBlock)
            txtSurFace = font.render(str(idx), True, (0, 0, 0), (128, 50, 50))
            w = txtSurFace.get_width()
            h = txtSurFace.get_height()
            mainSurface.blit(
                txtSurFace, (center[0] - w // 2, center[1] - h // 2))

        return mainSurface

    def _fillNum(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.array[y, x] != -1:
                    self.array[y, x] = self.countBoomAround(x, y)

        # print(self.array)

    def showAllBoom(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.statusArray[y, x] == 0 and self.array[y, x] == -1:
                    self.statusArray[y, x] = 1

    def setFlag(self, x, y):
        self.flags[y, x] = 1

    def getStatusFlag(self, x, y):
        return self.flags[y, x]

    def removeFlag(self, x, y):
        self.flags[y, x] = 0

    def checkWin(self):
        return self.numOfClose == self.numOfBoom
