from api.abstractions import CellType, ProvinceType, TerritoryType


def get_neighboards(cell: CellType, direction: tuple[int, int] = None) -> list[CellType]:
    if direction is None:
        neightboards = set((cell.add(0, 1), cell.add(1, 0), cell.add(0, -1), cell.add(-1, 0)))
    else:
        neightboards = set()

        x, y = direction

        if x:
            neightboards.add(cell.add(x, 0))
        if y: 
            neightboards.add(cell.add(0, y))

    return neightboards


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

    def get_expand_cells(self, direction: tuple[int, int] = None) -> set[CellType]:
        cells = set()
        
        for cell in self.contour_cells:
            for neighboard in get_neighboards(cell, direction):
                if neighboard.is_free():                    
                    cells.add(neighboard)

        free_cells = set(filter(lambda c: c.is_free(), cells))

        if direction is None:
            return free_cells
        
        x, y = direction
        return set(filter(
            lambda c: (c.add(-x, 0, self) in self.contour_cells if x else True) and (c.add(0, -y, self) in self.contour_cells if y else True), free_cells
        ))

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

    def extend(self, direction: tuple[int, int], size: int) -> None:
        new_province = self.territory.create_province(self.get_expand_cells(direction))

        for _ in range(size):
            new_province.expand(new_province.get_expand_cells(direction))

    def get_center_position(self) -> tuple[int, int]:
        min_x = min(self.contour_cells, key=lambda c: c.position[0]).position[0]
        max_x = max(self.contour_cells, key=lambda c: c.position[0]).position[0]
        min_y = min(self.contour_cells, key=lambda c: c.position[1]).position[1]
        max_y = max(self.contour_cells, key=lambda c: c.position[1]).position[1]
        
        return int((max_x + min_x) // 2), int((max_y + min_y) // 2)
