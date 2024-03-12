from api.abstractions import PlayerType, ProvinceType, TerritoryType

from .Province import Province


class Territory(TerritoryType):
    def __init__(self, player: PlayerType) -> None:
        self.player = player

        self.provinces = set()

    def create_province(self, position: tuple[int, int]) -> ProvinceType:
        province = Province(self)
        province.add_cell(position)

        self.provinces.add(province)

        return province
