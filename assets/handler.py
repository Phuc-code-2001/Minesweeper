from assets.board import Board


class Handler:
    def __init__(self, game):
        self.game = game
        self.board = Board(game)
        self.initialized = 0
        self.winGame = 0

    def reset(self):
        self.board = Board(self.game)
        self.initialized = 0
        self.winGame = 0

    def init(self):
        self.board._initializeMap()

    def draw(self):
        self.board.draw()
        if self.isWin():
            self.game.window.congratulate.draw(self.game.window.DISPLAYSURF)
            self.game.window.congratulate.update()
        if self.game.gameover:
            self.game.window.overtext.draw(self.game.window.DISPLAYSURF)
            self.game.window.overtext.update()

    def leftmouseclicked(self, pos):
        x = pos[0] // self.board.sizeBlock
        y = pos[1] // self.board.sizeBlock
        if self.initialized:
            self.board.statusArray[y, x] = 1
            self.board.numOfClose -= 1
            if self.board.array[y, x] == 0:
                self.board.floodFill(x, y)
            elif self.board.array[y, x] == -1:
                self.board.showAllBoom()
                self.game.gameover = True
        else:
            self.board.statusArray[y, x] = 1
            self.board.numOfClose -= 1
            self.board._initializeBoom(x, y)
            self.board._fillNum()
            self.board.floodFill(x, y)
            self.board._initializeMap()
            self.initialized = 1

    def rightmouseclicked(self, pos):
        if self.initialized:
            x = pos[0] // self.board.sizeBlock
            y = pos[1] // self.board.sizeBlock
            if not self.board.getStatusFlag(x, y):
                self.board.setFlag(x, y)
            else:
                self.board.removeFlag(x, y)

    def isWin(self):
        return self.board.checkWin()
