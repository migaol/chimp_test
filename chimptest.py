from typing import Tuple
from settings import *
from square import Square
from menu import Menu, PlusButton
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

        self.square_size = self.calc_square_size()
        self.board_offset = self.calc_board_offset()
        self.squares = None
        
        self.state = 'ready'
        
        self.times = {
            'memorize': [],
            'total': []
        }

        self.menu = pg.sprite.GroupSingle(Menu())

        self.font_title = pg.font.Font(FONT, FONTSIZE*2)
        self.font_subtitle = pg.font.Font(FONT, FONTSIZE)

        self.create_board()
        self.create_squares()

    def calc_square_size(self) -> int:
        return min(
            (SCREEN_HEIGHT - (self.rows+1)*SQR_MARGIN) // self.rows,
            (BOARD_WIDTH - (self.cols+1)*SQR_MARGIN) // self.cols,
            SQR_MAX_SIZE
        )

    def calc_board_offset(self) -> pg.Vector2:
        board_width = self.cols*self.square_size + (self.cols+1)*SQR_MARGIN
        board_height = self.rows*self.square_size + (self.rows+1)*SQR_MARGIN
        return pg.Vector2(BOARD_WIDTH // 2 - board_width // 2, SCREEN_HEIGHT // 2 - board_height // 2)

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
        if self.squares:
            self.surface.fill('black')
            for square in self.squares:
                square.kill()
        else: self.squares = pg.sprite.Group()

        for ri,r in enumerate(self.board):
            for ci,c in enumerate(r):
                # if c == 0: continue
                pos = pg.Vector2(
                    ci*(self.square_size + SQR_MARGIN) + SQR_MARGIN,
                    ri*(self.square_size + SQR_MARGIN) + SQR_MARGIN
                ) + self.board_offset
                square = Square(pos, self.square_size, c)
                self.squares.add(square)

    def end_level(self) -> None:
        if self.state == 'game': self.state = 'ready'
        self.currentnum = 1
        self.create_board()
        self.create_squares()
        self.menu.sprite.stop_time()

    def start_level(self) -> None:
        self.surface.fill('black')
        self.state = 'game'
        self.menu.sprite.reset_time()

    def next_level(self) -> None:
        self.level += 1
        self.times['total'].append(self.menu.sprite.get_time())
        self.end_level()

    def fail_level(self) -> None:
        self.strikes -= 1
        if self.strikes == 0:
            self.state = 'game_over'
            self.export_stats()
        self.end_level()

    def click(self, mouse_pos: Tuple[int, int]) -> None:
        menu: Menu = self.menu.sprite
        menu_clicked = menu.click(mouse_pos)
        if self.state == 'ready':
            if not menu_clicked:
                self.start_level()
        else:
            square: Square
            for square in self.squares:
                if square.collidepoint(mouse_pos):
                    if square.num == self.currentnum:
                        if self.currentnum == 1: self.times['memorize'].append(menu.get_time())
                        if self.currentnum == self.level: self.next_level()
                        else:
                            square.click()
                            self.currentnum += 1
                    else:
                        self.fail_level()
                    break

        if menu_clicked:
            self.rows = menu.row_slider.val
            self.cols = menu.col_slider.val
            self.square_size = self.calc_square_size()
            self.board_offset = self.calc_board_offset()
            self.level = DEFAULT_LEVEL
            self.end_level()

    def draw_menu(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        self.menu.update(mouse_pos)
        self.menu.draw(self.surface)

    def draw_squares(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        self.squares.update(mouse_pos, (self.currentnum == 1))
        self.squares.draw(self.surface)

    def draw_ready_screen(self) -> None:
        text1 = self.font_title.render(f"Level {self.level}", True, 'white')
        text1_rect = text1.get_rect(center=(BOARD_WIDTH//2, SCREEN_HEIGHT//2))
        self.surface.blit(text1, text1_rect)

        text2 = self.font_subtitle.render(f"Strikes: {self.strikes}", True, 'white')
        text2_rect = text2.get_rect(center=(BOARD_WIDTH//2, SCREEN_HEIGHT//2 + text1_rect.height))
        self.surface.blit(text2, text2_rect)

        text3 = self.font_subtitle.render(f"Click to continue", True, 'white')
        text3_rect = text3.get_rect(center=(BOARD_WIDTH//2, text2_rect.bottom + text2_rect.height))
        self.surface.blit(text3, text3_rect)

    def run(self) -> None:
        self.draw_menu()
        if self.state == 'ready':
            self.draw_ready_screen()
        elif self.state == 'game':
            self.draw_squares()
        elif self.state == 'game_over':
            self.draw_game_over()

    def export_stats(self) -> None:
        with open('stats.txt', 'w') as f:
            f.write(f"Level\tMemorization Time\tTotal Time\n")
            for i in range(self.level-1):
                level_str = f"{i+1:<5}"
                memorization_time_str = f"{self.times['memorize'][i]:<18}"
                total_time_str = f"{self.times['total'][i]}\n"
                f.write(f"{level_str}\t{memorization_time_str}\t{total_time_str}")

    def draw_game_over(self) -> None:
        text1 = self.font_title.render(f"Game Over", True, 'white')
        text1_rect = text1.get_rect(center=(BOARD_WIDTH//2, SCREEN_HEIGHT//2))
        self.surface.blit(text1, text1_rect)

        text2 = self.font_subtitle.render(f"You reached level {self.level}", True, 'white')
        text2_rect = text2.get_rect(center=(BOARD_WIDTH//2, SCREEN_HEIGHT//2 + text1_rect.height))
        self.surface.blit(text2, text2_rect)

        text3 = self.font_subtitle.render(f"Your stats can be viewed in 'stats.txt' in the root directory", True, 'white')
        text3_rect = text3.get_rect(center=(BOARD_WIDTH//2, text2_rect.bottom + text2_rect.height))
        self.surface.blit(text3, text3_rect)