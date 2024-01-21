from typing import Tuple
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

        self.square_size = (SCREEN_HEIGHT // self.rows) - 2*(SQR_MARGIN + SQR_STROKE)

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
                pos = pg.Vector2(
                    ci*(self.square_size + SQR_MARGIN + SQR_STROKE) + SQR_MARGIN + SQR_STROKE,
                    ri*(self.square_size + SQR_MARGIN + SQR_STROKE) + SQR_MARGIN + SQR_STROKE
                )
                square = Square(pos, self.square_size, c)
                self.squares.add(square)

    def next_level(self) -> None:
        self.level += 1
        self.currentnum = 1
        self.create_board()
        self.create_squares()

    def fail_level(self) -> None:
        self.strikes -= 1
        self.currentnum = 1
        self.create_board()
        self.create_squares()

    def click(self, mouse_pos: Tuple[int, int]) -> None:
        square: Square
        for square in self.squares:
            if square.is_clicked(mouse_pos):
                if square.num == self.currentnum:
                    if self.currentnum == self.level: self.next_level()
                    else:
                        square.num = 0
                        self.currentnum += 1
                else:
                    self.fail_level()
                break

    def draw_board(self) -> None:
        pass

    def draw_squares(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        self.squares.update(mouse_pos)
        self.squares.draw(self.surface)

    def run(self) -> None:
        self.draw_board()
        self.draw_squares()