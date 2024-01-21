from settings import *
from square import Square
import pygame as pg
from random import randint

class ChimpTest:
    def __init__(self, surface: pg.Surface, rows: int, cols: int, level: int, strikes: int) -> None:
        self.surface = surface

        self.rows = min(max(1,rows),MAX_ROWS)
        self.cols = min(max(1,cols),MAX_COLS)
        self.max_level = self.rows * self.cols
        self.level = max(1,level)
        self.strikes = strikes
        self.currentnum = 1

        self.square_size = (SCREEN_HEIGHT // self.rows) - 2*(SQUARE_MARGIN + SQUARE_STROKE)

        self.create_board()
        self.create_squares()

    def create_board(self) -> None:
        board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for num in range(1, self.level+1):
            while True:
                r = randint(0,self.rows-1)
                c = randint(0,self.cols-1)
                if board[r][c] == 0:
                    board[r][c] = num
                    break
        self.board = board

    def create_squares(self) -> None:
        self.squares = pg.sprite.Group()
        for ri,r in enumerate(self.board):
            for ci,c in enumerate(r):
                pos = pg.Vector2(ci*(self.square_size + SQUARE_MARGIN + SQUARE_STROKE) + SQUARE_MARGIN + SQUARE_STROKE,
                                 ri*(self.square_size + SQUARE_MARGIN + SQUARE_STROKE) + SQUARE_MARGIN + SQUARE_STROKE)
                square = Square(pos, self.square_size, c)
                self.squares.add(square)

    def check_cell(self, row: int, col: int) -> bool:
        return (self.board[row][col] == self.currentnum)
    
    def next_level(self) -> None:
        self.level += 1
        self.currentnum = 1
        self.create_board()

    def fail_level(self) -> None:
        self.currentnum = 1
        self.create_board()

    def draw_board(self) -> None:
        pass

    def draw_square(self) -> None:
        pass

    def draw_num(self) -> None:
        pass

    def run(self) -> None:
        self.squares.draw(self.surface)
        self.squares.update(self.surface)