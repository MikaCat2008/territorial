from sdk.abstractions import CellType, GameType, PlayerType
from sdk.cell import Cell
from sdk.player import Player
from sdk.territory import Territory


class Game(GameType):
    UNREACHABLE_TERRITORY = Territory(None)

    def __init__(self, w: int, h: int) -> None:
        self.w = w
        self.h = h
        self.players = []

        self.cells = {}

    def add_cell(self, cell: CellType) -> CellType:
        self.cells[cell.position] = cell

        return cell

    def get_cell(self, position: tuple[int, int]) -> CellType:
        if position in self.cells:
            return self.cells[position]
        
        x, y = position

        if x < 0 or y < 0 or x >= self.w or y >= self.h:
            return Cell(position, self.UNREACHABLE_TERRITORY)
        else:
            return self.add_cell(Cell(position, None))

    def create_player(self, name: str, color: tuple[int, int, int]) -> PlayerType:
        return Player.create(name, color, self)