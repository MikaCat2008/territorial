from api.abstractions import CellType, GameType, CellsMapType
from api.models import Cell, Player, FREE_CELL, UNREACHABLE_CELL


class CellsMap(CellsMapType):
    def __init__(self, w: int, h: int) -> None:
        self.w = w
        self.h = h
        self.cells = [[Cell(x, y, FREE_CELL) for x in range(w)] for y in range(h)]

    def __getitem__(self, point: tuple[int, int]) -> CellType:
        x, y = point

        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return Cell(x, y, UNREACHABLE_CELL)

        return self.cells[y][x]


class Game(GameType):
    def __init__(self, w: int, h: int) -> None:
        self.cells = CellsMap(w, h)
        self.players = []

    def create_player(self, name: str, color: tuple[int, int, int]) -> Player:
        return Player.create(name, color, self)
