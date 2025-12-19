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

