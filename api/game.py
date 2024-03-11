from api.abstractions import GameType
from api.models import Player


class Game(GameType):
    def __init__(self, w: int, h: int) -> None:
        self.w = w
        self.h = h
        self.players = []

        self.free_points = set([(x, y) for y in range(h) for x in range(w)])

    def filter_free(self, points: list[tuple[int, int]]) -> list[tuple[int, int]]:
        return points & self.free_points

    def create_player(self, name: str, color: tuple[int, int, int]) -> Player:
        return Player.create(name, color, self)
