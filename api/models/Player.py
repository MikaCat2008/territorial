from api.abstractions import GameType, PlayerType

from .Territory import Territory


class Player(PlayerType):
    def __init__(self, id: int, name: str, game: GameType) -> None:
        self.id = id
        self.name = name
        self.territory = Territory(self)

        self.game = game

    @classmethod
    def create(cls, name: str, game: GameType = None) -> PlayerType:
        if game is None:
            return Player(None, name, None)
        
        players = game.players
        
        id = len(players)
        player = Player(id, name, game)

        players.append(player)

        return player
