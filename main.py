import pygame as pg

from api.abstractions import CellType, PlayerType
from api.game import Game, GameType

CELL_SIZE = 20
GAME_WIDTH, GAME_HEIGHT = 40, 40

CELL_PATH = ((0, 0), (0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1))


def get_cell_by_mouse_pos() -> CellType:
    mx, my = pg.mouse.get_pos()
    x, y = int(mx / CELL_SIZE), int(my / CELL_SIZE)

    return game.cells[x, y]


def color_mod(color: tuple[int, int, int], n: int) -> tuple[int, int, int]:
    r, g, b = color
    
    return min(max(0, r + n), 255), min(max(0, g + n), 255), min(max(0, b + n), 255)


def sort_cells(cells: list[tuple[int, int]]) -> list[tuple[int, int]]:
    i = 0
    cells_set = set(cells)
    next_cell = cells[0]
    alt_cell = None
    sorted_cells = [None] * len(cells)

    while cells_set:
        if next_cell is None:
            i += 1
            next_cell = alt_cell
            alt_cell = None

        cells_set.remove(next_cell)
        sorted_cells[i] = next_cell

        x, y = next_cell
        next_cell = None

        for ox, oy in CELL_PATH:            
            cell = x + ox, y + oy
            
            if cell in cells_set:
                if next_cell:
                    alt_cell = cell

                    continue

                i += 1
                next_cell = cell

    return sorted_cells


def draw_cells(game: GameType, screen: pg.SurfaceType, s_player: PlayerType) -> None:
    for player in game.players:
        cells = [(c.x, c.y) for c in player.territory.cells]

        if not cells:
            continue

        color = player.color

        min_x = min(cells, key=lambda c: c[0])[0]
        max_x = max(cells, key=lambda c: c[0])[0] + 1
        min_y = min(cells, key=lambda c: c[1])[1]
        max_y = max(cells, key=lambda c: c[1])[1] + 1

        territory_surface = pg.Surface((max_x, max_y), pg.SRCALPHA)
        territory_surface.fill((255, 255, 255, 0))

        # sorted_cells = sort_cells([(c[0] - min_x, c[1] - min_y) for c in cells])

        if player is s_player:
            color = color_mod(color, 50)

        # pg.draw.polygon(territory_surface, color, sorted_cells, 0)
        # pg.draw.polygon(territory_surface, color_mod(color, -50), sorted_cells, 1)

        for cell in [(c[0] - min_x, c[1] - min_y) for c in cells]:
            territory_surface.set_at(cell, color)

        screen.blit(pg.transform.scale_by(territory_surface, CELL_SIZE), (min_x * CELL_SIZE, min_y * CELL_SIZE))


def main() -> None:
    player = None

    while 1:
        screen.fill((255, 255, 255))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEMOTION:
                ...
            elif event.type == pg.MOUSEBUTTONDOWN:
                cell = get_cell_by_mouse_pos()

                if player is None:
                    if cell.territory is not None:
                        player = cell.territory.player
                elif cell.territory is not player.territory:
                    target = None
                    if cell.territory:
                        target = cell.territory.player
                    
                    r, _, l = pg.mouse.get_pressed()

                    if r:
                        player.attack(target)
                    elif l:
                        for _ in range(5):
                            player.attack(target)
                else:
                    player = None

        draw_cells(game, screen, player)

        pg.display.flip()
        pg.display.set_caption(f"{clock.get_fps():.1f} fps")

        clock.tick(60)


if __name__ == "__main__":
    game = Game(GAME_WIDTH, GAME_HEIGHT)
    clock = pg.time.Clock()
    screen = pg.display.set_mode((GAME_WIDTH * CELL_SIZE, GAME_HEIGHT * CELL_SIZE))
    
    p1 = game.create_player("P1", (200, 0, 0))
    p2 = game.create_player("P2", (0, 200, 0))
    p3 = game.create_player("P3", (0, 0, 200))

    p1.spawn((5, 5))
    p2.spawn((23, 20))
    p3.spawn((27, 23))

    for _ in range(5):
        p1.attack()

    for _ in range(5):
        p2.attack()

    for _ in range(5):
        p3.attack()

    main()
