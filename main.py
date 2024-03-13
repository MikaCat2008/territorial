import math as m, time as t, collections as c

import pygame as pg

from api.abstractions import CellType, ProvinceType
from api.game import Game

WIDTH, HEIGHT = 200, 100
CELL = 5
EXPAND_SIZE = 100
PROVINCE_AREA = 300


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


def draw_territories() -> None:
    surface = pg.Surface((WIDTH, HEIGHT))
    surface.fill((255, 255, 255))

    pixel_array = pg.PixelArray(surface)

    for player in game.players:
        for province in player.territory.provinces:
            color = player.color
            
            if province is attack_province:
                color = color_mod(color, 20)

            contour_positions = set(cell.position for cell in province.contour_cells)

            for position in flood_fill(contour_positions, province):
                pixel_array[position] = to_int(color)

            for position in contour_positions:
                pixel_array[position] = to_int(color_mod(color, -50))

    del pixel_array

    screen.blit(pg.transform.scale_by(surface, CELL), (0, 0))


def expand(province: ProvinceType, direction: tuple[int, int], repeat: int) -> None:
    expands.append([(direction, province) for _ in range(repeat)])


def process_expands() -> None:
    global expands, expanding_belt
    
    for provinces in expands:
        direction, province = provinces[-1]

        cells = expanding_belt.get(province, set())

        if not cells:
            area = province.area
            free_area = PROVINCE_AREA - area

            expand_cells = province.get_expand_cells(direction)

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


def get_angle(position1: tuple[int, int], position2: tuple[int, int]) -> float:
    x1, y1 = position1
    x2, y2 = position2

    a_r = m.atan2(y2 - y1, x2 - x1)
    a_r = a_r * 180 / m.pi + 90
    
    if a_r > 180:
        a_r = a_r - 360

    return a_r


def get_direction(province: ProvinceType, cell: CellType) -> None:
    position1 = province.get_center_position()
    position2 = cell.position

    angle = get_angle(position1, position2)

    if -25.5 < angle <= 25.5:
        direction = (0, -1)
    elif 25.5 < angle <= 67.5:
        direction = (1, -1)
    elif 67.5 < angle <= 112.5:
        direction = (1, 0)
    elif 112.5 < angle <= 157.5:
        direction = (1, 1)
    elif 157.5 < angle or angle <= -157.5:
        direction = (0, 1)
    elif -157.5 < angle <= -112.5:
        direction = (-1, 1)
    elif -112.5 < angle <= -67.5:
        direction = (-1, 0)
    elif -67.5 < angle <= -25.5:
        direction = (-1, -1)

    return direction


def extend(province: ProvinceType, direction: tuple[int, int], size: int) -> None:
    province.extend(direction, size)


def main() -> None:
    global attack_province, target_province

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            # elif event.type == pg.MOUSEMOTION:
            #     cell = get_cell_by_mouse_pos()

            #     if attack_province:
            #         print(get_angle(attack_province.get_center_position(), cell.position))

            elif event.type == pg.MOUSEBUTTONDOWN:
                button = event.button

                if button == 1:
                    cell = get_cell_by_mouse_pos()

                    if cell.province is None:
                        continue
                    if cell.province is attack_province:
                        attack_province = None

                        continue

                    attack_province = cell.province

            elif event.type == pg.MOUSEBUTTONUP:
                button = event.button

                if button == 1:
                    cell = get_cell_by_mouse_pos()

                    if attack_province and cell.province is None:
                        direction = get_direction(attack_province, cell)
                        
                        if attack_province.area < PROVINCE_AREA:
                            expand(attack_province, direction, 5)
                        else:
                            extend(attack_province, direction, 5)

                        attack_province = None

                        continue

        process_expands()        
        draw_territories()

        if attack_province:
            x, y = attack_province.get_center_position()
            pg.draw.rect(screen, (0, 0, 0), (x * CELL, y * CELL, CELL, CELL))

        pg.display.flip()
        pg.display.set_caption(f"{int(clock.get_fps())} fps")

        clock.tick(60)


if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT)
    clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH * CELL, HEIGHT * CELL))

    expands = []
    expanding_belt = c.defaultdict(set)

    attack_province = None
    target_province = None

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
