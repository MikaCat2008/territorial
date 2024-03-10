from __future__ import annotations


class PlayerType:
    id: int
    name: str
    territory: TerritoryType

    game: GameType


class CellType:
    x: int
    y: int

    type: int
    territory: TerritoryType


class TerritoryType:
    player: PlayerType

    cells: list[CellType]


class CellsMapType:
    cells: list[list[CellType]]


class GameType:
    cells: CellsMapType
    players: list[PlayerType]
