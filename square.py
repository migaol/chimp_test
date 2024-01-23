from typing import Tuple
from settings import *
import pygame as pg

class Square(pg.sprite.Sprite):
    def __init__(self, pos: pg.Vector2, size: int, num: int) -> None:
        super().__init__()
        self.image = pg.Surface((size, size), pg.SRCALPHA)
        self.fill = SQR_CLR_DEFAULT
        self.image.fill(self.fill)
        self.rect = self.image.get_rect(topleft = pos)
        self.corner_radius = SQR_STROKE
        self.num = num
        self.is_clicked = False

        self.font = pg.font.Font(FONT, self.rect.width//3*2)
        self.text = self.font.render(str(self.num), True, 'black')
        self.text_rect = self.text.get_rect(center=(self.rect.width//2, self.rect.height//2))

    def click(self) -> None:
        self.num = 0
        self.fill = SQR_CLR_CLICKED
        self.is_clicked = True

    def update(self, mouse_pos: Tuple[int, int], memorization_phase: bool = False) -> None:
        if not self.is_clicked:
            self.fill = SQR_CLR_HLIGHT if self.rect.collidepoint(mouse_pos) else SQR_CLR_DEFAULT
        self.image.fill(self.fill)
        if self.num != 0 and memorization_phase: self.image.blit(self.text, self.text_rect)

    def collidepoint(self, mouse_pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)