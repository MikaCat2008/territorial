from sdk.abstractions import CellType, TerritoryType


class Cell(CellType):
    def __init__(self, position: tuple[int, int], territory: TerritoryType) -> None:
        self.position = position
        self.territory = territory

    def get(self, position: tuple[int, int]) -> CellType:
        return self.territory.get_cell(position)

    def add(self, ox: int, oy: int) -> CellType:
        x, y = self.position
        
        return self.get((x + ox, y + oy))
    
    def is_free(self) -> bool:
        return self.territory is None

    def __repr__(self) -> str:
        return f"{self.position}"
