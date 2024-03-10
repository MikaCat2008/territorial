from api.game import Game

GAME_SIZE = 10, 10

game = Game(*GAME_SIZE)
player1 = game.create_player("Adolf1")
player2 = game.create_player("Adolf2")

player1.spawn((4, 2))
player2.spawn((4, 7))

player1.attack()
player1.attack()
player2.attack()
player2.attack()


def draw() -> None:
    s = ""
    
    for y in range(GAME_SIZE[1]):
        for x in range(GAME_SIZE[0]):
            s += str(game.cells[x, y])
        s += "\n"

    print(s)


draw()
