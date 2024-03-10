from api.abstractions import CellType, PlayerType, TerritoryType
from api.cell import FREE_CELL, PLAYER_BORDER_CELL, PLAYER_TERRITORY_CELL


class Territory(TerritoryType):
    def __init__(self, player: PlayerType) -> None:
        self.player = player

        self.cells = set()

    def set_border_cell(self, x: int, y: int) -> None:
        cell = self.player.game.cells[x, y]
        
        cell.type = PLAYER_BORDER_CELL
        cell.territory = self
        self.cells.add(cell)

    def set_territory_cell(self, x: int, y: int) -> None:
        cell = self.player.game.cells[x, y]

        cell.type = PLAYER_TERRITORY_CELL
        self.cells.remove(cell)

    def remove_cell(self, x: int, y: int) -> None:
        cell = self.player.game.cells[x, y]

        cell.type = FREE_CELL
        self.cells.remove(cell)

    def get_cells_around(self) -> set[CellType]:
        cells = set()

        for cell in self.cells:
            cells_around = cell.get_cells_around()
            
            for _cell in cells_around:
                cells.add(_cell)

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
    
    def clear(self) -> None:
        cells = self.cells

        min_x = min(cells, key=lambda c: c.x).x
        max_x = max(cells, key=lambda c: c.x).x + 1
        min_y = min(cells, key=lambda c: c.y).y
        max_y = max(cells, key=lambda c: c.y).y + 1

        for row in self.player.game.cells.cells[min_y:max_y]:            
            for cell in row[min_x:max_x]:
                x = cell.x
                y = cell.y

                if cell.type == PLAYER_BORDER_CELL and cell.territory is self:
                    self.remove_cell(x, y)
                elif cell.type == PLAYER_TERRITORY_CELL and cell.territory is self:
                    self.player.game.cells[x, y].type = FREE_CELL

    def spawn(self, x: int, y: int) -> None:
        self.set_border_cell(x, y)

    def occupate(self, new_cells: list[CellType], excess_cells: list[CellType]) -> None:
        for new_cell in new_cells:
            x = new_cell.x
            y = new_cell.y
            
            self.set_border_cell(x, y)

        for excess_cell in excess_cells:
            x = excess_cell.x
            y = excess_cell.y

            self.set_territory_cell(x, y)
