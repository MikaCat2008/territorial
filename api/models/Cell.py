from api.abstractions import CellType, ProvinceType


class Cell(CellType):
    def __init__(self, position: tuple[int, int], province: ProvinceType) -> None:
        self.position = position
        self.province = province

    def get(self, position: tuple[int, int], _province: ProvinceType = None) -> CellType:
        if _province is None:
            return self.province.get_cell(position)
        return _province.get_cell(position)

    def add(self, ox: int, oy: int, _province: ProvinceType = None) -> CellType:
        x, y = self.position
        
        return self.get((x + ox, y + oy), _province)
    
    def is_free(self) -> bool:
        return self.province is None

    def __repr__(self) -> str:
        return f"{self.position}"
