from api.abstractions import CellType, TerritoryType

FREE_CELL = 0
UNREACHABLE_CELL = 1
PLAYER_BORDER_CELL = 2
PLAYER_TERRITORY_CELL = 3


class Cell(CellType):
    def __init__(self, x: int, y: int, type: int, territory: TerritoryType = None) -> None:
        self.x = x
        self.y = y
        self.type = type
        self.territory = territory

    def is_excess(self, target: TerritoryType = None) -> bool:
        for cell in self.get_cells_around():
            is_free_cell = cell.type == FREE_CELL
            is_enemy_cell = cell.type == PLAYER_BORDER_CELL and cell.territory is not self.territory
            is_target_cell = (is_enemy_cell and cell.territory is not target)
            is_unreachable_cell = cell.type == UNREACHABLE_CELL

            if target:
                if is_unreachable_cell or is_free_cell or is_target_cell:
                    return False
            else:
                if is_enemy_cell or is_unreachable_cell:
                    return False
        return True
    
    def is_inside_territory(self) -> bool:
        cells = self.get_cells_around()
        
        return all(
            cell.type in (PLAYER_BORDER_CELL, PLAYER_TERRITORY_CELL) and cell.territory is self.territory
            for cell in cells
        )

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
        elif self.type == UNREACHABLE_CELL:
            return "X"
        elif self.type == PLAYER_BORDER_CELL:
            return "@"
        elif self.type == PLAYER_TERRITORY_CELL:
            return "."

    def __repr__(self) -> str:
        return f"\"{str(self)}\"({self.x} {self.y})"
