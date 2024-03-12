from api.abstractions import CellType, ProvinceType, TerritoryType


def get_neighboards(cell: CellType) -> list[CellType]:
    return set((cell.add(0, 1), cell.add(1, 0), cell.add(0, -1), cell.add(-1, 0)))


class Province(ProvinceType):
    def __init__(self, territory: TerritoryType) -> None:
        self.area = 0
        self.territory = territory
        
        self.contour_cells = set()

    def get_cell(self, position: tuple[int, int]) -> CellType:
        return self.territory.player.game.get_cell(position)

    def add_cell(self, position: tuple[int, int]) -> None:
        cell = self.get_cell(position)

        cell.province = self
        
        self.area += 1
        self.contour_cells.add(cell)

    def get_expand_cells(self) -> set[CellType]:
        cells = set()
        
        for cell in self.contour_cells:
            for neighboard in get_neighboards(cell):
                if neighboard.is_free():                    
                    cells.add(neighboard)

        return set(filter(lambda c: c.is_free(), cells))

    def clear_excess(self) -> None:
        excess_cells = set()

        for cell in self.contour_cells:
            neighboards = get_neighboards(cell)
            is_excess = True

            for neighboard in neighboards:
                if neighboard.province is not self:
                    is_excess = False

            if is_excess:
                excess_cells.add(cell)

        self.contour_cells -= excess_cells

    def expand(self, expand_cells: set[CellType]) -> None:
        self.area += len(expand_cells)
        self.contour_cells |= expand_cells
        
        for cell in expand_cells:
            cell.province = self

        self.clear_excess()
