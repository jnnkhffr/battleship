"""
Tests for the Board class.
"""

import pytest
from src.battleship_game import Board


class TestBoardInitialization:
    """Tests for board initialization."""

    def test_board_creates_empty_grid(self, empty_board):
        """Board should be initialized with empty cells."""
        assert len(empty_board.grid) == 10
        assert len(empty_board.grid[0]) == 10
        assert all(cell == 0 for row in empty_board.grid for cell in row)

    def test_board_has_correct_dimensions(self, empty_board):
        """Board should have correct dimensions."""
        assert empty_board.cols == 10
        assert empty_board.rows == 10


class TestShipPlacement:
    """Tests for ship placement."""

    def test_can_place_ship_on_empty_board(self, empty_board):
        """Ship should be placeable on an empty board."""
        result = empty_board.can_place_ship(x=0, y=0, size=3, orientation="hor")
        assert result is True

    def test_cannot_place_ship_out_of_bounds_horizontal(self, empty_board):
        """Ship should not be placeable outside the board (horizontal)."""
        result = empty_board.can_place_ship(x=8, y=0, size=3, orientation="hor")
        assert result is False

    def test_cannot_place_ship_out_of_bounds_vertical(self, empty_board):
        """Ship should not be placeable outside the board (vertical)."""
        result = empty_board.can_place_ship(x=0, y=8, size=3, orientation="ver")
        assert result is False

    def test_cannot_place_ship_on_occupied_cell(self, board_with_ship):
        """Ship should not be placeable on an occupied cell."""
        # Board already has a ship at (2,3) horizontally with size=3
        result = board_with_ship.can_place_ship(x=2, y=3, size=2, orientation="hor")
        assert result is False

    def test_cannot_place_ship_too_close_to_existing_ship(self, board_with_ship):
        """Ships must have at least 1 cell distance between them."""
        # Board has a ship at (2,3) horizontally
        # Try to place a ship directly above it
        result = board_with_ship.can_place_ship(x=2, y=2, size=2, orientation="hor")
        assert result is False

    @pytest.mark.parametrize(
        "x,y,size,orientation,expected",
        [
            (0, 0, 1, "hor", True),  # Single cell
            (9, 9, 1, "hor", True),  # Corner
            (0, 0, 10, "hor", True),  # Full row
            (0, 0, 10, "ver", True),  # Full column
            (5, 5, 3, "hor", True),  # Middle horizontal
            (5, 5, 3, "ver", True),  # Middle vertical
        ],
    )
    def test_valid_placements(self, empty_board, x, y, size, orientation, expected):
        """Test various valid placements."""
        result = empty_board.can_place_ship(x, y, size, orientation)
        assert result == expected

    def test_place_ship_marks_cells(self, empty_board):
        """place_ship should mark cells as occupied."""
        empty_board.place_ship(x=1, y=1, size=3, orientation="hor")
        assert empty_board.grid[1][1] == 1
        assert empty_board.grid[1][2] == 1
        assert empty_board.grid[1][3] == 1
        assert empty_board.grid[1][4] == 0  # Adjacent cell should remain empty


class TestHitAndMiss:
    """Tests for hits and misses."""

    def test_hit_marks_cell_as_hit(self, empty_board):
        """hit() should mark a cell as hit."""
        empty_board.HIT_SOUND(x=5, y=5)
        assert empty_board.grid[5][5] == 3

    def test_miss_marks_cell_as_miss(self, empty_board):
        """miss() should mark a cell as a miss."""
        empty_board.MISS_SOUND(x=3, y=3)
        assert empty_board.grid[3][3] == 2

    def test_sunk_marks_ship_as_sunk(self, submarine):
        """sunk() should mark all ship cells as sunk."""
        board = Board()
        submarine.position = (2, 2)
        submarine.orientation = "hor"
        board.place_ship(2, 2, submarine.size, "hor")

        board.sunk(submarine)
        assert board.grid[2][2] == 4
