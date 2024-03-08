from api.game import Game

game = Game()
player0 = game.create_player("Adolf0")
player1 = game.create_player("Adolf1")

print(player0.id, player0.name)
print(player1.id, player1.name)
