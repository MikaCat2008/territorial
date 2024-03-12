from api.abstractions import GameType, PlayerType, ProvinceType

from .Territory import Territory


class Player(PlayerType):
    def __init__(self, id: int, name: str, color: tuple[int, int, int], game: GameType) -> None:
        self.id = id
        self.name = name
        self.color = color
        self.territory = Territory(self)

        self.game = game

    def set_capital(self, position: tuple[int, int], size: int) -> ProvinceType:
        capital = self.territory.create_province(position)

        for _ in range(size):
            capital.expand(capital.get_expand_cells())
        
        return capital

    @classmethod
    def create(cls, name: str, color: tuple[int, int, int], game: GameType = None) -> PlayerType:
        if game is None:
            return Player(None, name, color)
        
        players = game.players
        
        id = len(players)
        player = Player(id, name, color, game)

        players.append(player)

        return player
