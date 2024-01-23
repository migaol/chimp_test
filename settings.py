import pygame as pg
pg.font.init()

SCREEN_HEIGHT = 900
BOARD_WIDTH = 1200
MENU_WIDTH = 300
SCREEN_WIDTH = BOARD_WIDTH + MENU_WIDTH

SQR_MARGIN = 10
SQR_STROKE = 5
SQR_CLR_DEFAULT = 'white'
SQR_CLR_HLIGHT = 'lightgray'
SQR_CLR_CLICKED = 'black'

MENU_CLR = 'gray'

FONT = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
FONTSIZE = 36

MAX_ROWS = 6
MAX_COLS = 10
DEFAULT_STRIKES = 3

KEY_QUIT = pg.K_ESCAPE