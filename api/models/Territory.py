from api.abstractions import CellType, PlayerType, TerritoryType
from api.cell import FREE_CELL, PLAYER_BORDER_CELL


class Territory(TerritoryType):
    def __init__(self, player: PlayerType) -> None:
        self.player = player

        self.cells = []

    def set_cell(self, x: int, y: int, cell_type: int) -> None:
        cell = self.player.game.cells[x, y]
        
        self.cells.append(cell)
        cell.type = cell_type
        cell.territory = self

    def get_cells_around(self) -> list[CellType]:
        cells = []

        for cell in self.cells:
            cells_around = cell.get_cells_around()
            
            for _cell in cells_around:
                cells.append(_cell)

        return cells

    def get_free_cells_around(self) -> list[CellType]:
        cells = self.get_cells_around()

        return list(filter(lambda c: c.type == FREE_CELL, cells))

    def get_occupatable_cells(self, target: PlayerType = None) -> tuple[list[CellType], list[CellType]]:
        if target is None:
            new_cells = self.get_free_cells_around()
        else:
            ...

        excess_cells = []

        for cell in self.cells:
            if cell.is_excess():
                excess_cells.append(cell)

        return new_cells, excess_cells
        

    def spawn(self, x: int, y: int) -> None:
        self.set_cell(x, y, PLAYER_BORDER_CELL)

    def occupate(self) -> None:
        ...
