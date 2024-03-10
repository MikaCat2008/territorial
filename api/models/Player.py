from api.abstractions import GameType, PlayerType

from .Territory import Territory


class Player(PlayerType):
    def __init__(self, id: int, name: str, color: tuple[int, int, int], game: GameType) -> None:
        self.id = id
        self.name = name
        self.color = color
        self.territory = Territory(self)

        self.game = game

    def spawn(self, point: tuple[int, int]) -> None:
        self.territory.spawn(*point)

    def expand(self) -> None:
        new_cells, excess_cells = self.territory.get_occupatable_cells()
        
        self.territory.occupate(new_cells, excess_cells)

    def occupate(self, target: PlayerType) -> None:
        new_cells, excess_cells = self.territory.get_occupatable_cells(target.territory)

        target.territory.remove(new_cells)

        self.territory.occupate(new_cells, excess_cells)

    def attack(self, target: PlayerType = None) -> None:
        if target is None:
            self.expand()
        else:
            self.occupate(target)

    @classmethod
    def create(cls, name: str, color: tuple[int, int, int], game: GameType = None) -> PlayerType:
        if game is None:
            return Player(None, name, color)
        
        players = game.players
        
        id = len(players)
        player = Player(id, name, color, game)

        players.append(player)

        return player
