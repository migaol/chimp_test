from settings import *
from chimptest import ChimpTest
import sys, time, tracemalloc
import pygame as pg

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pg.SCALED, vsync=1)
clock = pg.time.Clock()

tracemalloc.start()
speed = {'slowest': 0, 'avg': 0, 'frames': 0}
def renderspeed(run):
    t1 = time.time()
    run()
    t2 = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    speed['slowest'] = max(t2-t1, speed['slowest'])
    speed['avg'] = (speed['avg'] * speed['frames'] + (t2-t1)*1000) / (speed['frames'] + 1)
    speed['frames'] += 1
    print(f"frames: {speed['frames']}  " +
            f"TIME current: {(t2-t1)*1000:.4f}ms  " +
            f"avg: {speed['avg']:.4f}ms  " +
            f"peak: {speed['slowest']*1000:.4f}ms  " +
            f"MEMORY current: {current_mem/100:.3f}kb  peak: {peak_mem/100:.3f}kb")

game = ChimpTest(surface=screen, rows=DEFAULT_ROWS, cols=DEFAULT_COLS, level=DEFAULT_LEVEL, strikes=3)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == KEY_QUIT):
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONUP:
            mouse_pos = pg.mouse.get_pos()
            game.click(mouse_pos)

    # renderspeed(game.run)
    game.run()
    
    pg.display.update()
    clock.tick(60)