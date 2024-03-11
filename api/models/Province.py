from api.abstractions import ProvinceType, TerritoryType


def get_neighboards(point: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = point
    
    return set(((x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)))


class Province(ProvinceType):
    def __init__(self, territory: TerritoryType, is_capital: bool) -> None:
        self.territory = territory
        self.is_capital = is_capital
        
        self.contour_points = set()

    def add_point(self, point: tuple[int, int]) -> None:
        self.contour_points.add(point)

        self.territory.player.game.free_points.remove(point)

    def get_expand_points(self) -> list[tuple[int, int]]:
        points = set()
        free_points = self.territory.player.game.free_points
        
        for point in self.contour_points:
            for neighboard in get_neighboards(point):
                if neighboard not in self.contour_points and neighboard in free_points:                    
                    points.add(neighboard)

        return self.territory.player.game.filter_free(points)

    def clear_excess(self) -> None:
        game = self.territory.player.game
        free_points = game.free_points

        excess_points = set()

        for point in self.contour_points:
            neighboards = get_neighboards(point)
            is_excess = True

            for neighboard in neighboards:
                if neighboard in free_points:                    
                    is_excess = False
                elif neighboard not in self.contour_points and not is_point_inside(*neighboard, list(self.contour_points)):
                    is_excess = False   

            if is_excess:
                excess_points.add(point)

        self.contour_points -= excess_points

    def expand(self) -> None:
        expand_points = self.get_expand_points()
        self.contour_points |= expand_points
        
        self.territory.player.game.free_points -= expand_points

        self.clear_excess()
