import pygame as pg

from sdk import TerritoryType


def color_mod(color: tuple[int, int, int], n: int) -> tuple[int, int, int]:
    r, g, b = color

    return min(max(0, r + n), 255), min(max(0, g + n), 255), min(max(0, b + n), 255)


def expand_surface(
    game_surface: pg.SurfaceType, territory: TerritoryType, 
    new_cells: set[tuple[int, int]], excess_cells: set[tuple[int, int]]
) -> None:
    color = territory.player.color

    for cell in new_cells:
        game_surface.set_at(cell, color_mod(color, -50))

    for cell in excess_cells:
        game_surface.set_at(cell, color)


def reduce_surface(
    game_surface: pg.SurfaceType, territory: TerritoryType, 
    reduced_cells: set[tuple[int, int]], contour_cells: set[tuple[int, int]]
) -> None:
    color = territory.player.color

    for cell in reduced_cells:
        game_surface.set_at(cell, color)

    for cell in contour_cells:
        game_surface.set_at(cell, color_mod(color, -50))
