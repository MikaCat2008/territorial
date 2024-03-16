from collections import defaultdict

import pygame as pg

from sdk import TerritoryType
from render import expand_surface, reduce_surface

MAX_EXPANSION_SIZE = 1000


class ExpansionManager:
    expansions: defaultdict[tuple[TerritoryType, TerritoryType], int]
    expansions_belt: defaultdict[tuple[TerritoryType, TerritoryType], set[tuple[int, int]]]

    def __init__(self, game_surface: pg.SurfaceType) -> None:
        self.game_surface = game_surface
        
        self.expansions = defaultdict(int)
        self.expansions_belt = defaultdict(set)

    def expanse(
        self, 
        territory: TerritoryType, 
        target: TerritoryType | None = None
    ) -> None:
        self.expansions[territory, target] += 1

    def update(self) -> None:
        for expansion, value in list(self.expansions.items()):
            if self.expansions_belt[expansion]:
                continue

            attacker, target = expansion

            expansion_cells = attacker.get_expansion_cells(target)

            self.expansions[expansion] -= 1
            self.expansions_belt[expansion] |= expansion_cells
            
            if value == 1 or not self.expansions_belt[expansion]:
                del self.expansions[expansion]

        if not self.expansions_belt:
            return

        expansion_size = MAX_EXPANSION_SIZE // len(self.expansions_belt)
        expansed_cells = set()
        expansion_cells = set()
        
        for expansion, cells in list(self.expansions_belt.items()):
            attacker, target = expansion
            
            cells -= expansed_cells
            expansion_cells = set(list(cells)[:expansion_size])

            expansed_cells |= expansion_cells

            excess_cells = attacker.expand(expansion_cells)

            if target:
                contour_cells = target.reduce(expansion_cells)

                reduce_surface(
                    self.game_surface, target, expansion_cells, contour_cells
                )

            expand_surface(
                self.game_surface, attacker, expansion_cells, excess_cells
            )

            self.expansions_belt[expansion] -= expansion_cells

            if not self.expansions_belt[expansion]:
                del self.expansions_belt[expansion]
