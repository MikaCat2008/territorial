CELL_PATH = ((0, 0), (0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1))


def distance(position1: tuple[int, int], position2: tuple[int, int]) -> float:
    x1, y1 = position1
    x2, y2 = position2

    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def sort_positions(positions: list[tuple[int, int]]) -> list[tuple[int, int]]:
    i = 0
    positions_set = set(positions)
    next_position = positions[0]
    last_position = next_position
    alt_positions = set()
    sorted_positions = [None] * len(positions)

    while positions_set:
        if next_position is None:
            i += 1

            while not next_position:
                next_position = min(alt_positions, key=lambda p: distance(last_position, p))

                alt_positions.remove(next_position)

                if next_position not in positions_set:
                    next_position = None

        positions_set.remove(next_position)
        sorted_positions[i] = next_position

        x, y = next_position
        last_position = next_position
        next_position = None

        for ox, oy in CELL_PATH:
            position = x + ox, y + oy

            if position in positions_set:
                if next_position:
                    alt_positions.add(position)
                else:
                    i += 1
                    next_position = position

    return sorted_positions


r1 = sort_positions([
    (1, 0), (5, 0), (1, 4), 
    (2, 0), (0, 1), (0, 2), 
    (0, 0), (4, 1), (0, 3), 
    (3, 2), (4, 0), (3, 0), 
    (2, 3), (0, 5), (0, 4)
])

print(r1)
