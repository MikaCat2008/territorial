from api.abstractions import GameType
from api.context import Context
from api.models import PlayerModel


class Game(GameType):
    def __init__(self) -> None:
        self.players = []

        self.ctx = Context(self)

    def create_player(self, name: str) -> PlayerModel:
        return PlayerModel.create(name, ctx=self.ctx)
