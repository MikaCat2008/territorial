from api.abstractions import PlayerType, ProvinceType, TerritoryType

from .Province import Province


class Territory(TerritoryType):
    def __init__(self, player: PlayerType) -> None:
        self.player = player

        self.provinces = set()

    def create_province(self, point: tuple[int, int], is_capital: bool) -> ProvinceType:
        province = Province(self, is_capital)
        province.add_point(point)

        self.provinces.add(province)

        return province
