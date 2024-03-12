import time as t, collections as c

import pygame as pg

from api.abstractions import CellType, ProvinceType
from api.game import Game

WIDTH, HEIGHT = 200, 100
CELL = 5
EXPAND_SIZE = 100
PROVINCE_AREA = 500


def get_cell_by_mouse_pos() -> CellType:
    mx, my = pg.mouse.get_pos()

    return game.get_cell((int(mx / CELL), int(my / CELL)))


def get_neighboards(position: tuple[int, int]) -> set[tuple[int, int]]:
    x, y = position
    
    return ((x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y))


def flood_fill(contour_positions: set[tuple[int, int]], province: ProvinceType) -> set[tuple[int, int]]:
    filled_positions = set()
    positions_queue = c.deque(contour_positions)
    
    while positions_queue:
        position = positions_queue.pop()
        filled_positions.add(position)
        
        for neighboard in get_neighboards(position):
            if neighboard not in filled_positions and game.get_cell(neighboard).province is province:
                positions_queue.append(neighboard)

    return filled_positions


def color_mod(color: tuple[int, int, int], n: int) -> tuple[int, int, int]:
    r, g, b = color

    return min(max(0, r + n), 255), min(max(0, g + n), 255), min(max(0, b + n), 255)


def to_int(color: tuple[int, int, int]) -> int:
    r, g, b = color
    
    return r * 256 * 256 + g * 256 + b


def draw_territories(selected_province: ProvinceType) -> None:
    surface = pg.Surface((WIDTH, HEIGHT))
    surface.fill((255, 255, 255))

    pixel_array = pg.PixelArray(surface)

    for player in game.players:
        color = player.color

        for province in player.territory.provinces:
            if province is selected_province:
                color = color_mod(color, 20)

            contour_positions = set(cell.position for cell in province.contour_cells)

            for position in flood_fill(contour_positions, province):
                pixel_array[position] = to_int(color)

            for position in contour_positions:
                pixel_array[position] = to_int(color_mod(color, -50))

    del pixel_array

    screen.blit(pg.transform.scale_by(surface, CELL), (0, 0))


def expand(province: ProvinceType, repeat: int) -> None:
    expands.append([province for _ in range(repeat)])


def process_expands() -> None:
    global expands, expanding_belt
    
    for provinces in expands:
        province = provinces[0]

        cells = expanding_belt.get(province, set())

        if not cells:
            area = province.area
            free_area = PROVINCE_AREA - area

            expand_cells = province.get_expand_cells()

            if free_area > len(expand_cells):
                expanding_belt[province] |= expand_cells

                provinces.pop()
            else:
                expanding_belt[province] |= set(list(expand_cells)[:free_area])

                provinces.clear()

    expands = list(filter(bool, expands))

    expanded_cells = 0

    for province, cells in expanding_belt.items():
        expand_cells = set(list(cells)[:EXPAND_SIZE - expanded_cells])

        province.expand(expand_cells)

        expanded_cells -= len(expand_cells)
        expanding_belt[province] -= expand_cells

        if expanded_cells <= 0:
            break

    new_expanding_belt = c.defaultdict(set)
    new_expanding_belt.update({k: v for k, v in expanding_belt.items() if v})

    expanding_belt = new_expanding_belt


def main() -> None:
    province = None

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                cell = get_cell_by_mouse_pos()

                if province is None:
                    if cell.province is not None:
                        province = cell.province
                elif cell.province is not province:
                    target = None

                    if cell.province:
                        target = cell.province

                    button = event.button

                    if target is None:
                        if button == 1:
                            expand(province, 1)
                        elif button == 3:
                            expand(province, 5)
                else:
                    province = None

        process_expands()        

        draw_territories(province)

        pg.display.flip()
        pg.display.set_caption(f"{int(clock.get_fps())} fps")

        clock.tick(60)


if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT)
    clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH * CELL, HEIGHT * CELL))

    expands = []
    expanding_belt = c.defaultdict(set)

    player1 = game.create_player("", (200, 0, 0))
    capital1 = player1.set_capital((WIDTH // 2, HEIGHT // 2), 5)    

    player2 = game.create_player("", (0, 200, 0))
    capital2 = player2.set_capital((WIDTH // 2 - WIDTH // 4, HEIGHT // 2 - HEIGHT // 4), 5)  

    player3 = game.create_player("", (0, 0, 200))
    capital3 = player3.set_capital((WIDTH // 2 + WIDTH // 4, HEIGHT // 2 - HEIGHT // 4), 5) 

    player4 = game.create_player("", (0, 200, 200))
    capital4 = player4.set_capital((WIDTH // 2 - WIDTH // 4, HEIGHT // 2 + HEIGHT // 4), 5) 

    player5 = game.create_player("", (200, 0, 200))
    capital5 = player5.set_capital((WIDTH // 2 + WIDTH // 4, HEIGHT // 2 + HEIGHT // 4), 5) 

    main()
