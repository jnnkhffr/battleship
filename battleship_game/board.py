import pygame
from itertools import product
from battleship_game.config import (
    GRID_COLS,
    GRID_ROWS,
    BLOCK_SIZE,
    COLOR_BG,
    COLOR_GRID,
    COLOR_SHIP,
    COLOR_MISS,
    COLOR_HIT,
    COLOR_SUNK,
    SHIP_MARGIN,
)


class Board:
    """
    Represents a Battleship game board with 10*10 grid,
    handles ship placement and track shots

    Responsibilities:
    - Stores the map state (Integers: 0=Water, 1=Ship, 2=Miss, 3=Hit, 4=Sunk).
    - Validates ship placement (Checking bounds and margins).
    - Draws the grid to the screen.
    """

    def __init__(self):
        self.cols = GRID_COLS
        self.rows = GRID_ROWS
        self.block_size = BLOCK_SIZE

        # Grid: 0=background(water), 1=Ship, 2=Miss, 3=Hit, 4=Sunk
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def draw(self, surface: pygame.Surface, offset_x: int = 0) -> None:
        """
        Draws the grid on a given Pygame surface.

        First fills the surface with the background color and then renders all grid lines.

        Args:
            surface: Target surface to draw on.
            offset_x: horizontal offset for drawing (used for enemy board)

        """
        # Background
        rect = pygame.Rect(
            offset_x, 0, self.cols * self.block_size, self.rows * self.block_size
        )
        pygame.draw.rect(surface, COLOR_BG, rect)
        # Draw cells using product like a list
        for x, y in product(range(self.cols), range(self.rows)):
            rect = pygame.Rect(
                offset_x + x * self.block_size,
                y * self.block_size,
                self.block_size,
                self.block_size,
            )

            val = self.grid[y][x]
            cell_color = COLOR_BG  # Default water

            # grid value check to determine the cell-color
            if val == 1:
                cell_color = COLOR_SHIP
            elif val == 2:
                cell_color = COLOR_MISS
            elif val == 3:
                cell_color = COLOR_HIT
            elif val == 4:
                cell_color = COLOR_SUNK

            # Draw fill if ship has been placed
            if cell_color != COLOR_BG:
                pygame.draw.rect(surface, cell_color, rect)

            # Draw outline now so grid stay on top of the fill
            pygame.draw.rect(surface, COLOR_GRID, rect, 1)

    def can_place_ship(self, ship, x: int, y: int, orientation: str) -> bool:
        """
        Check if a ship can be placed at (x, y) with given size and orientation.

        Conditions:
        - Ship must be fully inside the board
        - Ship cells must be empty
        - All surrounding cells (1-cell margin) must be empty
        """
        dx = 1 if orientation == "hor" else 0
        dy = 1 if orientation == "ver" else 0

        # Boundary Checks
        # Calculate the tail of the ship
        tail_x = x + dx * (ship.size - 1)
        tail_y = y + dy * (ship.size - 1)

        # Fit check
        if tail_x >= self.cols or tail_y >= self.rows:
            return False

        # Collision check
        x_start = max(0, x - SHIP_MARGIN)
        y_start = max(0, y - SHIP_MARGIN)
        x_end = min(self.cols, tail_x + SHIP_MARGIN + 1)
        y_end = min(self.rows, tail_y + SHIP_MARGIN + 1)

        # Scan the box
        for check_y in range(y_start, y_end):
            for check_x in range(x_start, x_end):
                if self.grid[check_y][check_x] != 0:
                    return False
        return True

    def place_ship(self, x: int, y: int, orientation: str) -> None:
        """
        Place a ship on the board by marking its cells as occupied.

        Args:
            x: Starting column.
            y: Starting row.
            size: Ship length.
            orientation: "hor" or "ver".
        """
        dx = 1 if orientation == "hor" else 0
        dy = 1 if orientation == "ver" else 0

        for i in range(ship.size):
            self.grid[y + dy * i][x + dx * i] = 1

    def hit(self, x: int, y: int) -> None:
        """Marks the cell as a HIT"""
        self.grid[y][x] = 3

    def miss(self, x: int, y: int) -> None:
        """Marks the cell as a MISS"""
        self.grid[y][x] = 2

    def sunk(self, ship) -> None:
        """Marks the whole ship as SUNK"""
        sx, sy = ship.position
        dx = 1 if ship.orientation == "hor" else 0
        dy = 1 if ship.orientation == "ver" else 0

        for i in range(ship.size):
            self.grid[sy + dy * i][sx + dx * i] = 4
