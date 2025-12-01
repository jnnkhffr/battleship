from typing import List, Optional, Tuple
from battleship_game.ship import Ship
from battleship_game.config import FLEET_DATA, SHIP_DATA
import pygame
from battleship_game.config import BLOCK_SIZE


class Fleet:
    def __init__(self):
        self.ships: List[Ship] = []  # empty list
        self.ships_to_place: List[str] = list(FLEET_DATA)  # copy of config fleet list

    def try_place_ship(self, start_row: int, start_col: int):
        if not self.ships_to_place:
            return

        name = self.ships_to_place[0]  # Starts from top item of list
        size = SHIP_DATA[name]  # Use the config to get real size

        # Calculate coordinates
        coords = []
        for i in range(size):
            coords.append((start_row, start_col + i))  # horizontal placement

        # Create and Save
        new_ship = Ship(name, coords)
        self.ships.append(new_ship)

        # 5. Remove from List
        self.ships_to_place.pop(0)
        print(f"Placed {name} at {coords}")

    def draw(self, surface):
        for ship in self.ships:
            for r, c in ship.position:
                rect = pygame.Rect(
                    c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
                )
                pygame.draw.rect(surface, (255, 0, 0), rect)
