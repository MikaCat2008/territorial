from api.abstractions import CellType, GameType, CellsMapType
from api.cell import Cell, FREE_CELL, UNREACHEBLE_CELL
from api.models import Player


class CellsMap(CellsMapType):
    def __init__(self, w: int, h: int) -> None:
        self.w = w
        self.h = h
        self.cells_map = [[Cell(x, y, FREE_CELL) for x in range(w)] for y in range(h)]

    def __getitem__(self, point: tuple[int, int]) -> CellType:
        x, y = point

        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return Cell(x, y, UNREACHEBLE_CELL)

        return self.cells_map[y][x]


class Game(GameType):
    def __init__(self, w: int, h: int) -> None:
        self.cells = CellsMap(w, h)
        self.players = []

    def create_player(self, name: str) -> Player:
        return Player.create(name, self)
