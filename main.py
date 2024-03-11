import time

from api.game import Game

game = Game(1001, 1001)

player = game.create_player(None, (255, 0, 0))

capital = player.set_capital((500, 500))


for _ in range(200):
    t = time.time()
    
    le = len(capital.get_expand_points())
    capital.expand()

    print(le, time.time() - t)


def draw() -> None:
    _map = [[" "] * 10 for _ in range(10)]

    for player in game.players:
        for region in player.territory.provinces:
            for x, y in region.contour_points:
                _map[y][x] = "@"

    print("\n".join("".join(line) for line in _map))


# draw()
