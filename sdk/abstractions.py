from __future__ import annotations


class PlayerType:
    id: int
    name: str
    color: tuple[int, int, int]
    territory: TerritoryType

    game: GameType


class TerritoryType:
    id: int
    player: PlayerType

    contour_cells: set[TerritoryType]


class GameType: 
    w: int
    h: int

    cells: list[list[int]]
    players: dict[int, PlayerType]
