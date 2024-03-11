from __future__ import annotations


class PlayerType:
    id: int
    name: str
    color: tuple[int, int, int]
    territory: TerritoryType

    game: GameType


class ProvinceType:
    territory: TerritoryType
    is_capital: bool

    contour_points: set[tuple[int, int]]


class TerritoryType:
    player: PlayerType

    provinces: set[ProvinceType]


class GameType: 
    w: int
    h: int
    players: list[PlayerType]

    free_points: set[tuple[int, int]]
