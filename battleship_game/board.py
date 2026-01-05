import pygame
from itertools import product

from battleship_game.config import (
    GRID_COLS,
    GRID_ROWS,
    BLOCK_SIZE,
    COLOR_BG,
    COLOR_GRID,
    COLOR_SHIP,
    SHIP_MARGIN,
)


class Board:
    """
    Represents a Battleship game board.

    Responsibilities:
    - Store grid state (0 = empty, 1 = ship)
    - Draw the board and ships
    - Validate ship placement with correct spacing rules
    """

    def __init__(
        self,
        cols: int = GRID_COLS,
        rows: int = GRID_ROWS,
        block_size: int = BLOCK_SIZE,
        bgcolor: tuple[int, int, int] = COLOR_BG,
        gridcolor: tuple[int, int, int] = COLOR_GRID,
    ) -> None:
        """
        Initializes a grid playing field.

        Args:
            cols: Number of columns in the grid.
            rows: Number of rows in the grid.
            block_size: Pixel size of a single block.
            bgcolor: Background color as RGB tuple.
            gridcolor: Line color of the grid as RGB tuple.
        """
        self.cols = cols
        self.rows = rows
        self.block_size = block_size
        self.bgcolor = bgcolor
        self.gridcolor = gridcolor

        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def draw(self, surface: pygame.Surface, offset_x: int = 0) -> None:
        """
        Draws the grid on a given Pygame surface.

        First fills the surface with the background color and then renders all grid lines.

        Args:
            surface: Target surface to draw on.
            offset_x: horizontal offset for drawing (used for enemy board)
        """
        rect = pygame.Rect(
            offset_x, 0, self.cols * self.block_size, self.rows * self.block_size
        )
        pygame.draw.rect(surface, self.bgcolor, rect)

        for x, y in product(range(self.cols), range(self.rows)):
            rect = pygame.Rect(
                offset_x + x * self.block_size,
                y * self.block_size,
                self.block_size,
                self.block_size,
            )
            pygame.draw.rect(surface, self.gridcolor, rect, 1)

            # draw ship
            if self.grid[y][x] == 1:
                pygame.draw.rect(surface, COLOR_SHIP, rect)

    def can_place_ship(self, x: int, y: int, size: int, orientation: str) -> bool:
        """
        Check if a ship can be placed at (x, y) with given size and orientation.

        Conditions:
        - Ship must be fully inside the board
        - Ship cells must be empty
        - All surrounding cells (1-cell margin) must be empty
        """
        dx = 1 if orientation == "hor" else 0
        dy = 1 if orientation == "ver" else 0

        # Ship hast to be within the gamefield
        for i in range(size):
            nx = x + dx * i
            ny = y + dy * i
            if not (0 <= nx < self.cols and 0 <= ny < self.rows):
                return False

        # Check that ship cells themselves are empty
        for i in range(size):
            nx = x + dx * i
            ny = y + dy * i
            if self.grid[ny][nx] == 1:
                return False

        # Check 1-cell margin around the whole ship
        # Define bounding box for ship + 1-cell margin

        max_x = x + dx * (size - 1) + SHIP_MARGIN
        max_y = y + dy * (size - 1) + SHIP_MARGIN

        # Clamp to board bounds
        min_x = max(0, x - SHIP_MARGIN)
        min_y = max(0, y - SHIP_MARGIN)
        max_x = min(self.cols - 1, max_x)
        max_y = min(self.rows - 1, max_y)

        for cy in range(min_y, max_y + 1):
            for cx in range(min_x, max_x + 1):
                # Skip cells that will be occupied by this ship
                is_ship_cell = False
                for i in range(size):
                    sx = x + dx * i
                    sy = y + dy * i
                    if cx == sx and cy == sy:
                        is_ship_cell = True
                        break
                if is_ship_cell:
                    continue

                # Any existing ship in the margin -> not allowed
                if self.grid[cy][cx] == 1:
                    return False

        return True

    def place_ship(self, x: int, y: int, size: int, orientation: str) -> None:
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

        for i in range(size):
            nx = x + dx * i
            ny = y + dy * i
            self.grid[ny][nx] = 1
