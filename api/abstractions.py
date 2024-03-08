from __future__ import annotations

PointType = tuple[int, int]


class PlayerType:
    id: int
    name: str

    game: GameType


class TerritoryType:
    player: PlayerType

    points: list[PointType]


class GameType:
    players: list[PlayerType]
