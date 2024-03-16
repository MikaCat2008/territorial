from sdk.abstractions import GameType, PlayerType
from sdk.territory import Territory


class Player(PlayerType):
    def __init__(self, id: int, name: str, color: tuple[int, int, int], game: GameType) -> None:
        self.id = id
        self.name = name
        self.color = color
        self.territory = Territory.create(self)

        self.game = game

    @classmethod
    def create(cls, name: str, color: tuple[int, int, int], game: GameType = None) -> PlayerType:
        if game is None:
            return Player(None, name, color)
        
        players = game.players
        
        id = len(players)
        player = Player(id, name, color, game)

        players[id] = player

        return player
