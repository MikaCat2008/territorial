import math as m, time as t, collections as c

import pygame as pg

from sdk import Game, CellType, PlayerType, TerritoryType

WIDTH, HEIGHT = 190, 100
CELL = 8
EXPAND_OCCUPATE_SIZE = 200


def get_cell_by_mouse_pos() -> CellType:
    mx, my = pg.mouse.get_pos()

    return game.get_cell((int(mx / CELL), int(my / CELL)))


def color_mod(color: tuple[int, int, int], n: int) -> tuple[int, int, int]:
    r, g, b = color

    return min(max(0, r + n), 255), min(max(0, g + n), 255), min(max(0, b + n), 255)


def set_capital(player: PlayerType, position: tuple[int, int], size: int) -> None:
    surface = pg.Surface((1, 1))
    rendered_territories[player.id] = surface, position

    territory = player.territory
    territory.add_cell(position)

    surface.set_at((0, 0), color_mod(player.color, -50))

    expand(territory, size)


def draw_territories() -> None:
    surface = pg.Surface((WIDTH, HEIGHT))
    surface.fill((255, 255, 255))

    for _, rendered_territory in rendered_territories.items():
        rendered, position = rendered_territory
        
        surface.blit(rendered, position)

    screen.blit(pg.transform.scale_by(surface, CELL), (0, 0))


def expand(territory: TerritoryType, repeat: int) -> None:
    expands.append([territory for _ in range(repeat)])


def occupate(attacker: TerritoryType, target: TerritoryType, repeat: int) -> None:
    target.attacker = attacker
    attacker.target = target

    occupates.append([(attacker, target) for _ in range(repeat)])


def expand_surface(
    surface: pg.SurfaceType, position: tuple[int, int], territory: TerritoryType, 
    new_cells: set[CellType], excess_cells: set[CellType]
) -> pg.SurfaceType:
    min_x = min(territory.contour_cells, key=lambda c: c.position[0]).position[0]
    max_x = max(territory.contour_cells, key=lambda c: c.position[0]).position[0]
    min_y = min(territory.contour_cells, key=lambda c: c.position[1]).position[1]
    max_y = max(territory.contour_cells, key=lambda c: c.position[1]).position[1]

    old_x, old_y = position

    new_w, new_h = max_x - min_x + 1, max_y - min_y + 1
    x_offset, y_offset = old_x - min_x, old_y - min_y
    new_position = old_x - x_offset, old_y - y_offset

    new_surface = pg.Surface((new_w, new_h), pg.SRCALPHA)
    new_surface.fill((255, 255, 255, 0))
    new_surface.blit(surface, (x_offset, y_offset))

    color = territory.player.color

    for cell in new_cells:
        x, y = cell.position

        new_surface.set_at((x - min_x, y - min_y), color_mod(color, -50))

    for cell in excess_cells:
        x, y = cell.position

        new_surface.set_at((x - min_x, y - min_y), color)

    return new_surface, new_position


def reduce_surface(
    surface: pg.SurfaceType, position: tuple[int, int], territory: TerritoryType, 
    reduce_cells: set[CellType], countour_cells: set[CellType]
) -> pg.SurfaceType:
    min_x = min(territory.contour_cells, key=lambda c: c.position[0]).position[0]
    max_x = max(territory.contour_cells, key=lambda c: c.position[0]).position[0]
    min_y = min(territory.contour_cells, key=lambda c: c.position[1]).position[1]
    max_y = max(territory.contour_cells, key=lambda c: c.position[1]).position[1]

    old_x, old_y = position

    new_w, new_h = max_x - min_x + 1, max_y - min_y + 1
    x_offset, y_offset = old_x - min_x, old_y - min_y
    new_position = old_x - x_offset, old_y - y_offset

    new_surface = pg.Surface((new_w, new_h), pg.SRCALPHA)
    new_surface.fill((255, 255, 255, 0))
    new_surface.blit(surface, (x_offset, y_offset))

    color = territory.player.color

    for cell in countour_cells:
        x, y = cell.position

        new_surface.set_at((x - min_x, y - min_y), color_mod(color, -50))

    for cell in reduce_cells:
        x, y = cell.position

        new_surface.set_at((x - min_x, y - min_y), (255, 255, 255, 0))

    return new_surface, new_position


def process_expands() -> None:
    global expands, expanding_belt
    
    for territories in expands:
        territory = territories[-1]

        cells = expanding_belt.get(territory, set())

        if not cells:
            expand_cells = territory.get_expand_cells()

            expanding_belt[territory] |= expand_cells

            territories.pop()

    expands = list(filter(bool, expands))
    expanded_cells = 0

    for territory, cells in expanding_belt.items():
        expand_cells = set(list(cells)[:EXPAND_OCCUPATE_SIZE - expanded_cells])
        excess_cells = territory.expand(expand_cells)

        surface, position = rendered_territories[territory.player.id]

        new_surface, new_position = expand_surface(
            surface, position, territory, expand_cells, excess_cells
        )

        rendered_territories[territory.player.id] = new_surface, new_position

        expanded_cells -= len(expand_cells)
        expanding_belt[territory] -= expand_cells

        if expanded_cells <= 0:
            break

    new_expanding_belt = c.defaultdict(set)
    new_expanding_belt.update({k: v for k, v in expanding_belt.items() if v})

    expanding_belt = new_expanding_belt


def process_occupates() -> None:
    global occupates, occupating_belt
    
    for attackers_targets in occupates:
        attacker_target = attackers_targets[-1]

        cells = occupating_belt.get(attacker_target, set())

        if not cells:
            attacker, target = attacker_target

            occupate_cells = attacker.get_occupate_cells(target)

            occupating_belt[attacker_target] |= occupate_cells

            attackers_targets.pop()

    occupates = list(filter(bool, occupates))
    occupated_cells = 0

    for attacker_target, cells in occupating_belt.items():
        attacker, target = attacker_target
        
        occupate_cells = set(list(cells)[:EXPAND_OCCUPATE_SIZE - occupated_cells])
        target_contour_cells = target.reduce(occupate_cells)
        excess_cells = attacker.expand(occupate_cells)

        surface, position = rendered_territories[attacker.player.id]

        new_surface, new_position = expand_surface(
            surface, position, attacker, occupate_cells, excess_cells
        )

        rendered_territories[attacker.player.id] = new_surface, new_position

        if target.contour_cells:
            surface, position = rendered_territories[target.player.id]

            new_surface, new_position = reduce_surface(
                surface, position, target, occupate_cells, target_contour_cells
            )

            rendered_territories[target.player.id] = new_surface, new_position
        else:
            del rendered_territories[target.player.id]

        occupated_cells -= len(occupate_cells)
        occupating_belt[attacker_target] -= occupate_cells

        if len(occupate_cells) < EXPAND_OCCUPATE_SIZE:
            target.attacker = None
            attacker.target = None

    new_occupating_belt = c.defaultdict(set)
    new_occupating_belt.update({k: v for k, v in occupating_belt.items() if v})

    occupating_belt = new_occupating_belt


def get_angle(position1: tuple[int, int], position2: tuple[int, int]) -> float:
    x1, y1 = position1
    x2, y2 = position2

    a_r = m.atan2(y2 - y1, x2 - x1)
    a_r = a_r * 180 / m.pi + 90
    
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

                    if territory is None:
                        territory = cell.territory

                        continue
                    if cell.territory is None:
                        continue
                    if cell.territory is territory:
                        territory = None

                        continue

            elif event.type == pg.MOUSEBUTTONUP:
                button = event.button

                cell = get_cell_by_mouse_pos()

                if territory is None or cell.territory is territory:
                    continue

                if cell.territory is None:
                    if button == 1:
                        expand(territory, 1)
                    elif button == 3:
                        expand(territory, 50)
                else:
                    enemy = cell.territory

                    if button == 1:
                        occupate(territory, enemy, 1)
                    elif button == 3:
                        occupate(territory, enemy, 50)

        process_expands()
        process_occupates()
        draw_territories()

        pg.display.flip()
        pg.display.set_caption(f"{int(clock.get_fps())} fps")

        clock.tick(60)


if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT)
    clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH * CELL, HEIGHT * CELL))

    expands = []
    occupates = []
    expanding_belt = c.defaultdict(set)
    occupating_belt = c.defaultdict(set)

    territory = None
    rendered_territories = {}

    player1 = game.create_player("", (200, 0, 0))
    set_capital(player1, (WIDTH // 2, HEIGHT // 2), 5)

    player2 = game.create_player("", (0, 200, 0))
    set_capital(player2, (WIDTH // 2 - WIDTH // 4, HEIGHT // 2 - HEIGHT // 4), 5)  

    player3 = game.create_player("", (0, 0, 200))
    set_capital(player3, (WIDTH // 2 + WIDTH // 4, HEIGHT // 2 - HEIGHT // 4), 5) 

    player4 = game.create_player("", (0, 200, 200))
    set_capital(player4, (WIDTH // 2 - WIDTH // 4, HEIGHT // 2 + HEIGHT // 4), 5) 

    player5 = game.create_player("", (200, 0, 200))
    set_capital(player5, (WIDTH // 2 + WIDTH // 4, HEIGHT // 2 + HEIGHT // 4), 5) 

    main()
