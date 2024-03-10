from api.abstractions import GameType, PlayerType

from .Territory import Territory


class Player(PlayerType):
    def __init__(self, id: int, name: str, game: GameType) -> None:
        self.id = id
        self.name = name
        self.territory = Territory(self)

        self.game = game

    def spawn(self, point: tuple[int, int]) -> None:
        self.territory.spawn(*point)

    def attack(self, target: PlayerType = None) -> None:
        new_cells, excess_cells = self.territory.get_occupatable_cells(target)

        # ...

        # print(len(new_cells))

        self.territory.occupate(new_cells, excess_cells)

    @classmethod
    def create(cls, name: str, game: GameType = None) -> PlayerType:
        if game is None:
            return Player(None, name, None)
        
        players = game.players
        
        id = len(players)
        player = Player(id, name, game)

        players.append(player)

        return player
