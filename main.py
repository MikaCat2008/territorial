import math as m, random as r

import pygame as pg

from sdk import Game, PlayerType
from sdk.territory import FREE_TERRITORY
from render import color_mod
from expansion import ExpansionManager

CELL = 2
WIDTH, HEIGHT = 1500 // CELL, 760 // CELL


def random_position() -> tuple[int, int]:
    x = r.randint(0, WIDTH - 1)
    y = r.randint(0, HEIGHT - 1)
    
    return x, y


def random_color() -> tuple[int, int, int]:
    red = r.randint(0, 255)
    g = r.randint(0, 255)
    b = r.randint(0, 255)
    
    return red, g, b


def get_cell_by_mouse_pos() -> int:
    mx, my = pg.mouse.get_pos()

    return game.cells[my // CELL][mx // CELL]


def set_capital(player: PlayerType, position: tuple[int, int], size: int) -> None:
    territory = player.territory

    territory.add_cell(position)
    game_surface.set_at(position, color_mod(player.color, -50))

    for _ in range(size):
        expansion_manager.expanse(territory)


def get_angle(position1: tuple[int, int], position2: tuple[int, int]) -> float:
    x1, y1 = position1
    x2, y2 = position2

    a_r = m.atan2(y2 - y1, x2 - x1) * 180 / m.pi + 90
    
    if a_r > 180:
        a_r = a_r - 360

    return a_r


def main() -> None:
    global territory

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                button = event.button

                if button == 1 or button == 3:
                    cell = get_cell_by_mouse_pos()

                    if cell == FREE_TERRITORY:
                        continue
                    if territory is None:
                        territory = cell

                        continue
                    if cell == territory:
                        territory = None

                        continue

            elif event.type == pg.MOUSEBUTTONUP:
                button = event.button

                cell = get_cell_by_mouse_pos()

                if territory is None or cell == territory:
                    continue

                attacker = game.players[territory].territory

                if cell == FREE_TERRITORY:
                    target = None
                else:
                    target = game.players[cell].territory
                
                if button == 1:
                    expansion_manager.expanse(attacker, target)
                elif button == 3:
                    for _ in range(50):
                        expansion_manager.expanse(attacker, target)

        expansion_manager.update()
        screen.blit(pg.transform.scale_by(game_surface, CELL), (0, 0))

        pg.display.flip()
        pg.display.set_caption(f"{int(clock.get_fps())} fps")

        clock.tick(60)


if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT)
    clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH * CELL, HEIGHT * CELL))
    game_surface = pg.Surface((WIDTH, HEIGHT))
    game_surface.fill((255, 255, 255))

    territory = None

    expansion_manager = ExpansionManager(game_surface)

    for _ in range(100):
        player = game.create_player(None, random_color())
        set_capital(player, random_position(), 50)

    main()
