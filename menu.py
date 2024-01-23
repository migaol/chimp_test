from typing import Any
from settings import *
import pygame as pg
import time

class Menu(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pg.Surface((MENU_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA)
        self.fill = 'white'
        self.image.fill(self.fill)
        self.rect = self.image.get_rect(topright=(SCREEN_WIDTH, 0))

        self.title_font = pg.font.Font(FONT, int(1.5*FONTSIZE))
        self.font = pg.font.Font(FONT, FONTSIZE)

        self.text_title = self.title_font.render('Chimp Test', True, 'black')
        self.text_title_rect = self.text_title.get_rect()
        self.text_title_rect.top = self.image.get_rect().top

        self.reset_time()

    def reset_time(self) -> None:
        self.start_time = time.time()
    
    def draw_time(self) -> int:
        t = round(time.time() - self.start_time, 2)
        text_time = self.font.render(f"{t:.2f}", True, 'black')
        text_time_rect = text_time.get_rect()
        text_time_rect.center = self.image.get_rect().center
        self.image.blit(text_time, text_time_rect)

    def update(self) -> None:
        self.image.fill(self.fill)
        self.image.blit(self.text_title, self.text_title_rect)
        self.draw_time()