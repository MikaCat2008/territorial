from sdk.abstractions import PlayerType, CellType, TerritoryType


def get_neighboards(cell: CellType) -> set[CellType]:
    return set((cell.add(0, 1), cell.add(1, 0), cell.add(0, -1), cell.add(-1, 0)))


class Territory(TerritoryType):
    def __init__(self, player: PlayerType) -> None:
        self.area = 0
        self.contour_cells = set()

        self.target0 = None
        self.attacker = None

        self.player = player
    
    def get_cell(self, position: tuple[int, int]) -> CellType:
        return self.player.game.get_cell(position)

    def add_cell(self, position: tuple[int, int]) -> None:
        cell = self.get_cell(position)

        cell.territory = self
        
        self.area += 1
        self.contour_cells.add(cell)

    def get_expand_cells(self) -> set[CellType]:
        cells = set()
        
        for cell in self.contour_cells:
            for neighboard in get_neighboards(cell):
                if neighboard.is_free():
                    cells.add(neighboard)

        return cells
    
    def get_occupate_cells(self, target: TerritoryType) -> set[CellType]:
        cells = set()
        
        for cell in self.contour_cells:
            for neighboard in get_neighboards(cell):
                if neighboard.territory is target:
                    cells.add(neighboard)

        return cells

    def clear_excess(self) -> set[CellType]:
        excess_cells = set()

        for cell in self.contour_cells:
            is_excess = True

            for neighboard in get_neighboards(cell):
                if neighboard.territory is not self:
                    is_excess = False

            if is_excess:
                excess_cells.add(cell)

        self.contour_cells -= excess_cells

        return excess_cells
    
    def fix_contour(self, reduce_cells: set[CellType]) -> set[CellType]:
        contour_cells = set()

        for cell in reduce_cells:
            for neighboard in get_neighboards(cell):
                if neighboard.territory is self and neighboard not in self.contour_cells:
                    contour_cells.add(neighboard)

        self.contour_cells |= contour_cells

        return contour_cells

    def expand(self, expand_cells: set[CellType]) -> set[CellType]:
        self.area += len(expand_cells)
        self.contour_cells |= expand_cells
        
        for cell in expand_cells:
            cell.territory = self

        return self.clear_excess()
    
    def reduce(self, reduce_cells: set[CellType]) -> set[CellType]:        
        fixed_contour = self.fix_contour(reduce_cells)
        
        self.area -= len(reduce_cells)
        self.contour_cells -= reduce_cells

        return fixed_contour
