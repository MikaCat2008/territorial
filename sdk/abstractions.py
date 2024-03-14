from __future__ import annotations


class CellType:
    position: tuple[int, int]
    territory: TerritoryType


class PlayerType:
    id: int
    name: str
    color: tuple[int, int, int]
    territory: TerritoryType

    game: GameType


class TerritoryType:
    player: PlayerType

    contour_cells: set[TerritoryType]


class GameType: 
    w: int
    h: int
    players: list[PlayerType]

    cells: dict[tuple[int, int], CellType]
