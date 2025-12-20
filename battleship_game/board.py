import pygame
from itertools import product

from battleship_game.config import GRID_COLS, GRID_ROWS, BLOCK_SIZE, COLOR_BG, COLOR_GRID


class Board:
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
        """
        rect = pygame.Rect(offset_x, 0, self.cols * self.block_size, self.rows * self.block_size)
        pygame.draw.rect(surface, self.bgcolor, rect)

        for x, y in product(range(self.cols), range(self.rows)):
            rect = pygame.Rect(
                offset_x +
                x * self.block_size,
                y * self.block_size,
                self.block_size,
                self.block_size
            )
            pygame.draw.rect(surface, self.gridcolor, rect, 1)

            # draw ship
            if self.grid[y][x] == 1:
                pygame.draw.rect(surface, (169, 169, 169), rect)


    def can_place_ship(self, x: int, y: int, size: int, orientation: str) -> bool:
                """Checks if you can place a ship with one grid between ships)."""

                dx = 1 if orientation == "hor" else 0
                dy = 1 if orientation == "ver" else 0

                # 1) Ship hast to be within the gamefield
                for i in range(size):
                    nx = x + dx * i
                    ny = y + dy * i
                    if not (0 <= nx < self.cols and 0 <= ny < self.rows):
                        return False

                # 2) Checks the distance
                for i in range(-1, size + 1):
                    for ox in (-1, 0, 1):
                        for oy in (-1, 0, 1):
                            nx = x + dx * i + ox
                            ny = y + dy * i + oy
                            if 0 <= nx < self.cols and 0 <= ny < self.rows:
                                if self.grid[ny][nx] == 1:
                                    return False

                return True

    def place_ship(self, x: int, y: int, size: int, orientation: str) -> None:
                """Enters the ship into the grid"""
                dx = 1 if orientation == "hor" else 0
                dy = 1 if orientation == "ver" else 0

                for i in range(size):
                    nx = x + dx * i
                    ny = y + dy * i
                    self.grid[ny][nx] = 1