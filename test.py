import time as t

from sdk import Game

game = Game(201, 201)
# players = [game.create_player(None, None) for _ in range(100)]

# capital_positions = [(x * 100, y * 100) for y in range(10) for x in range(10)]

# for player, position in zip(players, capital_positions):
#     player.territory.add_cell(position)


# total_time, total_cells = 0, 0
# for _ in range(100):
#     time = 0
#     cells = 0

#     for player in players:
#         t1 = t.time()
#         expansion_cells = player.territory.get_expansion_cells()

#         player.territory.expand(expansion_cells)
#         time += t.time() - t1

#         cells += len(expansion_cells)

#     print(f"{cells=}\t{time=}")
#     total_cells += cells
#     total_time += time

# print(f"{total_cells=}\t{total_time=}")


player = game.create_player(None, None)

player.territory.add_cell((200, 500))

# print(player.territory.get_expansion_cells())

t1 = t.time()

for _ in range(300):
    expansion_cells = player.territory.get_expansion_cells()
    player.territory.expand(expansion_cells)

print(t.time() - t1)

# expansion_cells = player.territory.get_expansion_cells()
# print(player.territory.expand(expansion_cells))
