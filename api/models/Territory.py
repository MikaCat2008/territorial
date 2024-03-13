from api.abstractions import PlayerType, ProvinceType, TerritoryType

from .Province import Province


class Territory(TerritoryType):
    def __init__(self, player: PlayerType) -> None:
        self.player = player

        self.provinces = set()

    def create_province(self, start_positions: set[tuple[int, int]]) -> ProvinceType:
        province = Province(self)
        province.expand(start_positions)

        self.provinces.add(province)

        return province
