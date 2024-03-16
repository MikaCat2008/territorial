from sdk.abstractions import GameType, PlayerType
from sdk.player import Player
from sdk.territory import FREE_TERRITORY, UNREACHABLE_TERRITORY


class Game(GameType):
    def __init__(self, w: int, h: int) -> None:
        self.w = w
        self.h = h
        
        self.cells = [[FREE_TERRITORY for _ in range(w)] for _ in range(h)]
        self.players = {}

    def get_cell(self, position: tuple[int, int]) -> int:
        x, y = position

        if x < 0 or y < 0 or x >= self.w or y >= self.h:
            return UNREACHABLE_TERRITORY
        return self.cells[y][x]

    def create_player(self, name: str, color: tuple[int, int, int]) -> PlayerType:
        return Player.create(name, color, self)
