from settings import *
import pygame as pg

class Square(pg.sprite.Sprite):
    def __init__(self, pos: pg.Vector2, size: int, num: int):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft = pos)
        self.num = num

        self.font = pg.font.Font(FONT, FONTSIZE)
        self.text = self.font.render(str(self.num), True, 'black')
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def update(self, surface: pg.Surface):
        if self.num != 0: surface.blit(self.text, self.text_rect.topleft)