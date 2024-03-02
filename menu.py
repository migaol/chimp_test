from typing import Any, Tuple
from settings import *
import pygame as pg
import time

class Button(pg.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int], size: int | Tuple[int, int], fill: str = BTN_CLR_DEFAULT) -> None:
        super().__init__()
        if type(size) is int: size = (size, size)
        self.image = pg.Surface(size, pg.SRCALPHA)
        self.fill = fill
        self.image.fill(self.fill)
        self.rect = self.image.get_rect(topleft=pos)
        self.disabled = False

        self.font = pg.font.Font(FONT, FONTSIZE)

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        if not self.disabled:
            self.fill = BTN_CLR_HLIGHT if self.rect.collidepoint(mouse_pos) else BTN_CLR_DEFAULT
        self.image.fill(self.fill)

    def disable(self) -> None:
        self.disabled = True
        self.fill = BTN_CLR_DISABLED

    def enable(self) -> None:
        self.disabled = False
    
    def draw_text(self, s: str) -> None:
        text = self.font.render(s, True, 'black')
        text_rect = text.get_rect()
        text_rect.center = self.image.get_rect().center
        self.image.blit(text, text_rect)

    def draw(self, surface: pg.surface) -> None:
        surface.blit(self.image, self.rect)

class PlusButton(Button):
    def __init__(self, pos: Tuple[int, int], fill: str = BTN_CLR_DEFAULT) -> None:
        super().__init__(pos, int(FONTSIZE * 1.5), fill)
    
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        super().update(mouse_pos)
        super().draw_text('+')

    def collidepoint(self, mouse_pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)

class MinusButton(Button):
    def __init__(self, pos: Tuple[int, int], fill: str = BTN_CLR_DEFAULT) -> None:
        super().__init__(pos, int(FONTSIZE * 1.5), fill)
    
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        super().update(mouse_pos)
        super().draw_text('-')
    
    def collidepoint(self, mouse_pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)

class PMSlider(pg.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int], default_val: int, min_val: int, max_val: int,
                    margin: int, internal_width: int) -> None:
        super().__init__()
        self.plus = PlusButton((margin, margin))
        self.minus = MinusButton((margin + self.plus.rect.width + internal_width, margin))

        size = (2*margin + self.plus.rect.width + internal_width + self.minus.rect.width,
                2*margin + self.plus.rect.height)
        self.image = pg.Surface(size, pg.SRCALPHA)
        self.image.fill(MENU_CLR)
        self.rect = self.image.get_rect(center=pos)

        self.font = pg.font.Font(FONT, FONTSIZE)

        self.min_val = min_val
        self.max_val = max_val
        self.val = default_val

    def translate_pos(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        return (pos[0] - self.rect.left, pos[1] - self.rect.top)

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        mouse_pos = self.translate_pos(mouse_pos)

        self.plus.update(mouse_pos)
        self.plus.draw(self.image)
        self.minus.update(mouse_pos)
        self.minus.draw(self.image)

        text = self.font.render(str(self.val), True, 'black')
        text_rect = text.get_rect()
        text_rect.center = self.image.get_rect().center
        self.image.blit(text, text_rect)

    def click(self, mouse_pos: Tuple[int, int]) -> bool:
        mouse_pos = self.translate_pos(mouse_pos)
        if self.plus.collidepoint(mouse_pos):
            self.val += 1
            self.minus.enable()
            if self.val >= self.max_val:
                self.plus.disable()
            if self.val > self.max_val:
                self.val = self.max_val
                return False
            self.image.fill(MENU_CLR)
            return True

        if self.minus.collidepoint(mouse_pos):
            self.val -= 1
            self.plus.enable()
            if self.val <= self.min_val:
                self.minus.disable()
            if self.val < self.min_val:
                self.val = self.min_val
                return False
            self.image.fill(MENU_CLR)
            return True

        return False

    def draw(self, surface: pg.surface) -> None:
        surface.blit(self.image, self.rect)

    def collidepoint(self, mouse_pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)

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
        self.text_title_rect = self.text_title.get_rect(center=(MENU_WIDTH//2, 50))

        self.time_state = 'stopped'

        self.row_slider = PMSlider(self.translate_pos((self.rect.centerx, 150)), DEFAULT_ROWS, 1, MAX_ROWS, 20, 60)
        self.col_slider = PMSlider(self.translate_pos((self.rect.centerx, 300)), DEFAULT_COLS, 1, MAX_COLS, 20, 60)

    def stop_time(self) -> None:
        self.time_state = 'stopped'

    def reset_time(self) -> None:
        self.time_state = 'running'
        self.start_time = time.time()
    
    def get_time(self) -> int:
        return round(time.time() - self.start_time, 2)

    def draw_time(self) -> int:
        if self.time_state == 'running':
            text_time = self.font.render(f"{self.get_time():.2f}", True, 'black')
            text_time_rect = text_time.get_rect()
            text_time_rect.center = self.image.get_rect().center
            self.image.blit(text_time, text_time_rect)

    def translate_pos(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        return (pos[0] - BOARD_WIDTH, pos[1])

    def click(self, mouse_pos: Tuple[int, int]) -> bool:
        mouse_pos = self.translate_pos(mouse_pos)
        if self.row_slider.collidepoint(mouse_pos):
            return self.row_slider.click(mouse_pos)
        if self.col_slider.collidepoint(mouse_pos):
            return self.col_slider.click(mouse_pos)
        return False
    
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        mouse_pos = self.translate_pos(mouse_pos)
        self.image.fill(self.fill)
        self.image.blit(self.text_title, self.text_title_rect)
        self.draw_time()

        self.row_slider.update(mouse_pos)
        self.row_slider.draw(self.image)
        self.col_slider.update(mouse_pos)
        self.col_slider.draw(self.image)