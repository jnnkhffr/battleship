import pygame
import random
from typing import List, Tuple, Set, Optional

from battleship_game.ship import Ship
from battleship_game.config import (
    GRID_ROWS,
    GRID_COLS,
    BLOCK_SIZE,
    FLEET_DATA,
    SHIP_DATA,
)


class EnemyFleet:
    def __init__(self):
        # 1. Store ships and the grid, just like the player
        self.ships: List[Ship] = []
        self.grid: List[List[Optional[Ship]]] = [
            [None] * GRID_COLS for _ in range(GRID_ROWS)
        ]

        # 2. Track hits and misses for the battle phase
        self.misses: Set[Tuple[int, int]] = set()
        self.hits: Set[Tuple[int, int]] = set()

        # 3. IMMEDIATELY place all ships randomly
        self.place_all_ships_randomly()

    def place_all_ships_randomly(self):
        """
        Loops through every ship in the standard fleet and tries to
        place it at a random valid location.
        """
        for ship_name in FLEET_DATA:
            placed = False

            # Keep trying random spots until one works
            while not placed:
                # A. Roll the dice
                row = random.randint(0, GRID_ROWS - 1)
                col = random.randint(0, GRID_COLS - 1)
                orientation = random.choice(["horizontal", "vertical"])
                size = SHIP_DATA[ship_name]

                # B. Calculate coordinates based on orientation
                coords = []
                for i in range(size):
                    if orientation == "horizontal":
                        coords.append((row, col + i))
                    else:  # vertical
                        coords.append((row + i, col))

                # C. Validate
                if self.is_position_valid(coords):
                    # Create the ship
                    new_ship = Ship(ship_name, coords)
                    self.ships.append(new_ship)

                    # Mark the grid
                    for r, c in coords:
                        self.grid[r][c] = new_ship

                    placed = True  # Exit the 'while' loop and move to the next ship

    def is_position_valid(self, coords: List[Tuple[int, int]]) -> bool:
        """Checks if a list of coordinates is on the board and empty."""
        for r, c in coords:
            # Check boundaries
            if not (0 <= r < GRID_ROWS and 0 <= c < GRID_COLS):
                return False
            # Check overlaps
            if self.grid[r][c] is not None:
                return False
        return True

    def receive_shot(self, row: int, col: int) -> str:
        """
        Processes a shot from the Player.
        Returns: 'MISS', 'HIT', 'SUNK', or 'ALREADY_SHOT'
        """
        if (row, col) in self.misses or (row, col) in self.hits:
            return "ALREADY_SHOT"

        ship = self.grid[row][col]

        if ship is None:
            self.misses.add((row, col))
            return "MISS"
        else:
            self.hits.add((row, col))
            ship.add_hit((row, col))
            if ship.is_sunk():
                return "SUNK"
            return "HIT"

    def draw(self, surface: pygame.Surface, x_offset: int, y_offset: int):
        """
        Draws the shots (Hits/Misses).
        IMPORTANT: We do NOT draw the ships themselves, because they are hidden!
        """
        # Draw Misses (Blue Dots)
        for r, c in self.misses:
            center_x = x_offset + (c * BLOCK_SIZE) + (BLOCK_SIZE // 2)
            center_y = y_offset + (r * BLOCK_SIZE) + (BLOCK_SIZE // 2)
            pygame.draw.circle(surface, (0, 0, 255), (center_x, center_y), 5)

        # Draw Hits (Orange/Red)
        for r, c in self.hits:
            rect = pygame.Rect(
                x_offset + c * BLOCK_SIZE,
                y_offset + r * BLOCK_SIZE,
                BLOCK_SIZE,
                BLOCK_SIZE,
            )

            # Check if the ship there is sunk
            ship = self.grid[r][c]

            if ship and ship.is_sunk():
                # Red Box for Sunk
                pygame.draw.rect(surface, (255, 0, 0), rect)
            else:
                # Orange Box for Hit
                pygame.draw.rect(surface, (255, 165, 0), rect)

            pygame.draw.rect(surface, (0, 0, 0), rect, 1)  # Border
