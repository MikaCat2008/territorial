CELL_PATH = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1))


def sort_cells(cells: list[tuple[int, int]]) -> list[tuple[int, int]]:
    i = 0
    cells_set = set(cells)
    next_cell = cells[0]
    alt_cell = None
    sorted_cells = [None] * len(cells)

    while cells_set:
        if next_cell is None:
            i += 1
            next_cell = alt_cell
            alt_cell = None

        cells_set.remove(next_cell)
        sorted_cells[i] = next_cell

        x, y = next_cell
        next_cell = None

        for ox, oy in CELL_PATH:            
            cell = x + ox, y + oy
            
            if cell in cells_set:
                if next_cell:
                    alt_cell = cell

                    continue

                i += 1
                next_cell = cell

    return sorted_cells


print(sort_cells([
    (3, 8), (5, 0), (9, 7), (8, 8), 
    (0, 5), (9, 4), (4, 1), (4, 9), 
    (6, 1), (7, 9), (1, 6), (10, 5), 
    (3, 2), (11, 5), (5, 10), (7, 2), 
    (6, 10), (2, 3), (10, 6), (2, 7), 
    (8, 3), (1, 4)

    # (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)

    # (0, 0), (1, 1), (2, 1), (1, 2), (0, 3)
]))
