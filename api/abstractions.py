from __future__ import annotations


class CellType:
    position: tuple[int, int]
    province: ProvinceType


class PlayerType:
    id: int
    name: str
    color: tuple[int, int, int]
    territory: TerritoryType

    game: GameType


class ProvinceType:
    area: int
    territory: TerritoryType

    contour_cells: set[CellType]


class TerritoryType:
    player: PlayerType

    provinces: set[ProvinceType]


class GameType: 
    w: int
    h: int
    players: list[PlayerType]

    cells: dict[tuple[int, int], CellType]
