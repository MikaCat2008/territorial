from api.abstractions import GameType, ContextType


class Context(ContextType):
    def __init__(self, game: GameType) -> None:
        self.game = game
