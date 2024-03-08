from api.abstractions import GameType, PlayerModelType
from api.context import Context


class PlayerModel(PlayerModelType):
    def __init__(self, id: int, name: str, game: GameType = None) -> None:
        self.id = id
        self.name = name

        self.game = game

    @classmethod
    def create(cls, name: str, ctx: Context = None) -> PlayerModelType:
        player_model = PlayerModel(None, name)
        
        if ctx is None:
            return player_model
        
        players = ctx.game.players
        player_model.id = len(players)
        players.append(player_model)

        return player_model
