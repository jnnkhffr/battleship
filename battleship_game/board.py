"""This file creates the game board."""
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
    COLOR_MISS,
    COLOR_HIT,
    COLOR_SUNK,
    COLOR_PREVIEW,
    ALPHA_PREVIEW,
)


class Board:
    """
    Represents a Battleship game board with grid states, drawing logic,
    and ship placement validation.
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
        Initializes a Battleship board with a 2D grid and visual settings.

        Args:
            cols: Number of columns in the grid.
            rows: Number of rows in the grid.
            block_size: Pixel size of a single block.
            bgcolor: Background color as RGB tuple.
            gridcolor: Grid line color as RGB tuple.
        """
        self.cols = cols
        self.rows = rows
        self.block_size = block_size
        self.bgcolor = bgcolor
        self.gridcolor = gridcolor

        # grid states (0 for empty, 1 for ship)
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def draw(
        self,
        surface: pygame.Surface,
        offset_x: int = 0,
        offset_y: int = 0,
        preview: dict | None = None,
        token_images=None,
        ship_images=None,
        fleet=None

    ) -> None:
        """
        Draw the board, grid lines, ships, hits, and misses onto a Pygame surface.

        Args:
            surface: The Pygame surface to draw on.
            offset_x: Horizontal drawing offset.
            offset_y: Vertical drawing offset.
            preview: Optional preview data for ship placement containing:
                x, y, size, orientation, alpha, valid.
        """
        # Background
        rect = pygame.Rect(
            offset_x, 0, self.cols * self.block_size, self.rows * self.block_size
        )
        pygame.draw.rect(surface, self.bgcolor, rect)

        # Ships
        if fleet and ship_images:
            for ship in fleet.ships:
                if ship.position is None:
                    continue

                img = ship_images.get(ship.name)
                if not img:
                    continue
                sx, sy = ship.position
                draw_x = offset_x + sx * self.block_size
                draw_y = sy * self.block_size
                draw_img = img
                if ship.orientation == "hor":
                    draw_img = pygame.transform.rotate(img, 90)

                surface.blit(draw_img, (draw_x, draw_y))

            # draw grid lines and tokens
        for x, y in product(range(self.cols), range(self.rows)):
                rect = pygame.Rect(
                        offset_x + x * self.block_size,
                        y * self.block_size,
                        self.block_size,
                        self.block_size,
                    )
                pygame.draw.rect(surface, self.gridcolor, rect, 1)
                val = self.grid[y][x]
                if token_images and val in token_images:
                    token = token_images[val]
                    token_rect = token.get_rect(center=rect.center)
                    surface.blit(token, token_rect)
                pygame.draw.rect(surface, self.gridcolor, rect, 1)



        if preview is not None:
            px = preview.get("x")
            py = preview.get("y")
            size = preview.get("size", 1)
            orientation = preview.get("orientation", "hor")
            alpha = preview.get("alpha", ALPHA_PREVIEW)
            valid = preview.get("valid", True)

            # choose color: ship color if valid else red-ish
            preview_color = COLOR_SHIP if valid else COLOR_PREVIEW

            dx = 1 if orientation == "hor" else 0
            dy = 1 if orientation == "ver" else 0

            cell_surf = pygame.Surface(
                (self.block_size, self.block_size), pygame.SRCALPHA
            )
            r, g, b = preview_color
            cell_surf.fill((r, g, b, alpha))

            for i in range(size):
                cx = px + dx * i
                cy = py + dy * i
                if 0 <= cx < self.cols and 0 <= cy < self.rows:

                    dest = (
                        offset_x + cx * self.block_size,
                        offset_y + cy * self.block_size,
                    )
                    surface.blit(cell_surf, dest)
                    # redraw grid border so lines stay visible
                    cell_rect = pygame.Rect(
                        dest[0], dest[1], self.block_size, self.block_size
                    )

    def can_place_ship(self, x: int, y: int, size: int, orientation: str) -> bool:
        """
        Check whether a ship can be placed at the given position.

        Args:
            x: Starting column of the ship.
            y: Starting row of the ship.
            size: Length of the ship.
            orientation: "hor" or "ver".

        Returns:
            True if the ship fits inside the board, all cells are empty,
            and the required 1-cell margin around the ship is free.
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
                is_ship_cell = False
                for i in range(size):
                    sx = x + dx * i
                    sy = y + dy * i
                    if cx == sx and cy == sy:
                        is_ship_cell = True
                        break
                if is_ship_cell:
                    continue

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

    # part from darshan
    def hit(self, x: int, y: int) -> None:
        """
        Mark a cell as a hit:

        Args:
            x: Column of the hit.
            y: ROW of the hit.
        """
        self.grid[y][x] = 3

    def miss(self, x: int, y: int) -> None:
        """Mark a cell as a miss."""
        self.grid[y][x] = 2

    def sunk(self, ship) -> None:
        """
        Mark all cells of a ship as sunk.

        Args:
            ship: Ship object containing position, size and orientation.
        """
        sx, sy = ship.position
        dx = 1 if ship.orientation == "hor" else 0
        dy = 1 if ship.orientation == "ver" else 0

        for i in range(ship.size):
            self.grid[sy + dy * i][sx + dx * i] = 4
