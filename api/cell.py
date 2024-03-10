from api.abstractions import CellType, TerritoryType

FREE_CELL = 0
UNREACHEBLE_CELL = 1
PLAYER_BORDER_CELL = 2
PLAYER_TERRITORY_CELL = 3


class Cell(CellType):
    def __init__(self, x: int, y: int, type: int, territory: TerritoryType = None) -> None:
        self.x = x
        self.y = y
        self.type = type
        self.territory = territory

    def is_excess(self) -> bool:
        for cell in self.get_cells_around():
            if (cell.type == PLAYER_BORDER_CELL and cell.territory is not self.territory) \
                or cell.type == UNREACHEBLE_CELL:
                return False
        return True

    def get_cells_around(self) -> list[CellType]:
        x = self.x
        y = self.y
        cells = self.territory.player.game.cells

        return [
            cells[x, y - 1],
            cells[x + 1,y ],
            cells[x, y + 1],
            cells[x - 1, y]
        ]

    def __str__(self) -> str:
        if self.type == FREE_CELL:
            return " "
        elif self.type == UNREACHEBLE_CELL:
            return "X"
        elif self.type == PLAYER_BORDER_CELL:
            return "@"
        elif self.type == PLAYER_TERRITORY_CELL:
            return "."

    def __repr__(self) -> str:
        return f"\"{str(self)}\"({self.x} {self.y})"
