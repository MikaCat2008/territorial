from api.abstractions import GameType
from api.models import Player


class Game(GameType):
    def __init__(self) -> None:
        self.players = []

    def create_player(self, name: str) -> Player:
        return Player.create(name, self)
