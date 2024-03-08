from api.abstractions import PlayerType, TerritoryType


class Territory(TerritoryType):
    def __init__(self, player: PlayerType) -> None:
        self.player = player
        
        self.points = []
