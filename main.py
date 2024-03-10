from api.game import Game

GAME_SIZE = 10, 10

game = Game(*GAME_SIZE)
player = game.create_player("Adolf")

player.spawn((9, 4))
player.attack()


def draw() -> None:
    s = ""
    
    for y in range(GAME_SIZE[1]):
        for x in range(GAME_SIZE[0]):
            s += str(game.cells[x, y])
        s += "\n"

    print(s)


draw()
