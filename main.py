from colorama import Fore

from api.game import Game

GAME_SIZE = 10, 10

game = Game(*GAME_SIZE)
player1 = game.create_player("Adolf1", Fore.GREEN)
player2 = game.create_player("Adolf2", Fore.BLUE)

player1.spawn((4, 2))
player2.spawn((4, 7))

player1.attack()
player1.attack()
player2.attack()
player2.attack()
player1.attack()
player2.attack()
player2.attack()

player2.attack(player1)
player2.attack(player1)
player2.attack(player1)
player2.attack(player1)
player2.attack(player1)


def draw() -> None:
    s = ""
    
    for y in range(GAME_SIZE[1]):
        for x in range(GAME_SIZE[0]):
            cell = game.cells[x, y]
            if cell.territory is None:
                color = ""
            else:
                color = cell.territory.player.color
            
            s += color + str(cell) + Fore.RESET
        s += "\n"

    print(s)


draw()
