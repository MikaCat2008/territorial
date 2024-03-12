from api.abstractions import CellType, ProvinceType


class Cell(CellType):
    def __init__(self, position: tuple[int, int], province: ProvinceType) -> None:
        self.position = position
        self.province = province

    def get(self, position: tuple[int, int]) -> CellType:
        return self.province.get_cell(position)

    def add(self, ox: int, oy: int) -> CellType:
        x, y = self.position
        
        return self.get((x + ox, y + oy))
    
    def is_free(self) -> bool:
        return self.province is None

    def __repr__(self) -> str:
        return f"{self.position}"
