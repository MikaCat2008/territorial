from __future__ import annotations


class PlayerModelType:
    id: int
    name: str

    game: GameType


class GameType:
    players: list[PlayerModelType]


class ContextType:
    game: GameType
