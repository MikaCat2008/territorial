from sdk.abstractions import PlayerType, TerritoryType

FREE_TERRITORY = -1
UNREACHABLE_TERRITORY = -2


class Territory(TerritoryType):
    def __init__(self, id: int, player: PlayerType) -> None:
        self.id = id
        self.area = 0
        self.contour_cells = set()

        self.player = player

    def get_cell(self, position: tuple[int, int]) -> int:
        return self.player.game.get_cell(position)

    def set_cell(self, position: tuple[int, int]) -> None:
        x, y = position
        
        self.player.game.cells[y][x] = self.id

    def add_cell(self, position: tuple[int, int]) -> None:
        self.area += 1
        self.set_cell(position)
        self.contour_cells.add(position)
    
    def get_neighbour_cells(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        x, y = position
        
        return ((x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y))

    def get_expansion_cells(self, target: TerritoryType = None) -> set[tuple[int, int]]:
        cells = set()
        
        for cell in self.contour_cells:
            for position in self.get_neighbour_cells(cell):
                if position in cells:
                    continue

                neighbour = self.get_cell(position)

                if target is None:
                    if neighbour == FREE_TERRITORY:
                        cells.add(position)
                else:
                    if neighbour == target.id:
                        cells.add(position)

        return cells

    def clear_excess(self, expand_cells: set[tuple[int, int]]) -> set[tuple[int, int]]:
        excess_cells = set()
        passed_cells = set()

        if len(expand_cells) * 4 < len(self.contour_cells):
            for cell in expand_cells:
                for position in self.get_neighbour_cells(cell):
                    if position in excess_cells:
                        continue

                    neighbour = self.get_cell(position)

                    if neighbour != self.id:
                        continue

                    for _position in self.get_neighbour_cells(position):
                        if _position in passed_cells:
                            continue

                        _neighbour = self.get_cell(_position)
                        passed_cells.add(_neighbour)

                        if _neighbour != self.id:
                            break

                    else:
                        excess_cells.add(position)
        else:
            for cell in self.contour_cells:
                for position in self.get_neighbour_cells(cell):
                    if position in passed_cells:
                        continue
                    
                    neighbour = self.get_cell(position)
                    passed_cells.add(position)

                    if neighbour != self.id:
                        break
                else:
                    excess_cells.add(cell)

        self.contour_cells -= excess_cells

        return excess_cells
    
    def fix_contour(self, reduce_cells: set[tuple[int, int]]) -> set[tuple[int, int]]:
        contour_cells = set()

        for cell in reduce_cells:
            for neighbour, position in self.get_neighbour_cells(cell):
                if neighbour == self.id and position not in self.contour_cells:
                    contour_cells.add(position)

        self.contour_cells |= contour_cells

        return contour_cells

    def expand(self, expand_cells: set[tuple[int, int]]) -> set[tuple[int, int]]:
        self.area += len(expand_cells)
        self.contour_cells |= expand_cells
        
        for cell in expand_cells:
            self.set_cell(cell)

        return self.clear_excess(expand_cells)

    def reduce(self, reduce_cells: set[tuple[int, int]]) -> set[tuple[int, int]]:        
        fixed_contour = self.fix_contour(reduce_cells)
        
        self.area -= len(reduce_cells)
        self.contour_cells -= reduce_cells

        return fixed_contour

    @classmethod
    def create(cls, player: PlayerType) -> TerritoryType:
        if player is None:
            return Territory(None)
        
        id = player.id
        territory = Territory(id, player)

        return territory
