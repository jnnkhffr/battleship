"""Different difficulty levels."""

from abc import ABC, abstractmethod
from battleship_game.config import GRID_COLS, GRID_ROWS
import random


class ShootingStrategy(ABC):
    """Abstract base class for all enemy shooting strategies."""

    # TODO: typing
    @abstractmethod
    def get_next_shot(self, opponent_board) -> tuple[int, int]:
        """
        Return the next shot coordinates based on the strategy.

        Args:
            opponent_board: The player's board used to evaluate shot choices.

        Returns:
            A tuple (x, y) representing the next target cell.
        """
        pass

    # TODO: typing
    def register_shot_result(self, x: int, y: int, hit: bool, sunk: bool) -> None:
        """
        Receive feedback about the last shot to update strategy states.

        Args:
            x: Column of the shot.
            y: Row of the shot.
            hit: True if the shot hit a ship.
            sunk: True if the shot sank a ship.
        """
        pass


class RandomShootingStrategy(ShootingStrategy):
    """Shooting strategy that selects random unshot cells."""

    def get_next_shot(self, opponent_board) -> tuple[int, int]:
        """
        Return a random valid shot that has not been fired before.

        Args:
            opponent_board: The player's board used to avoid repeated shots.

        Returns:
            A tuple (x, y) representing a random unshot cell.
        """
        while True:
            x = random.randint(0, GRID_COLS - 1)
            y = random.randint(0, GRID_ROWS - 1)

            if opponent_board.grid[y][x] not in [2, 3, 4]:
                return x, y


class HuntShootingStrategy(ShootingStrategy):
    """Shooting strategy that hunts around previous hits to find full ships."""

    def __init__(self) -> None:
        """Shooting strategy that hunts around previous hits to find full ships."""
        self.pending_hits: list[tuple[int, int]] = []
        self.hunt_direction = None

    def get_next_shot(self, opponent_board) -> tuple[int, int]:
        """
        Return the next shot using hunt logic or fallback scanning.

        Args:
            opponent_board: The player's board used to evaluate shot choices.

        Returns:
            A tuple (x, y) representing the next target cell.
        """
        if self.pending_hits:
            return self._target_mode(opponent_board)

        self._scan_for_hits(opponent_board)

        if self.pending_hits:
            return self._target_mode(opponent_board)

        return RandomShootingStrategy().get_next_shot(opponent_board)

    def register_shot_result(self, x: int, y: int, hit: bool, sunk: bool) -> None:
        """
        Update internal states based on the result of the last shot.

        Args:
            x: Column of the shot.
            y: Row of the shot.
            hit: True if the shot hit a ship.
            sunk: True if the shot sank a ship.
        """
        if hit:
            self.pending_hits.append((x, y))

        if sunk:
            self.pending_hits.clear()
            self.hunt_direction = None

    def _scan_for_hits(self, board) -> None:
        """
        Scan the board for existing hit markers to continue hunting.

        Args:
            board: The player's board used to detect previous hits.
        """
        self.pending_hits.clear()
        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                if board.grid[y][x] == 3:
                    self.pending_hits.append((x, y))

    def _target_mode(self, board) -> tuple[int, int]:
        """
        Attempt to continue shooting around known hits.

        Args:
            board: The player's board used to evaluate shot choices.

        Returns:
            A tuple (x, y) for the next target, or a fallback random shot.
        """
        if len(self.pending_hits) == 1:
            x, y = self.pending_hits[0]
            candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            shot = self._pick_valid(board, candidates)
            if shot:
                return shot

        if self.hunt_direction is None:
            self._determine_direction()

        if self.hunt_direction == "horizontal":
            return self._continue_horizontal(board)

        if self.hunt_direction == "vertical":
            return self._continue_vertical(board)

        return RandomShootingStrategy().get_next_shot(board)

    def _determine_direction(self) -> None:
        """Determine whether the ship is aligned horizontally or vertically."""
        if len(self.pending_hits) < 2:
            return
        (x1, y1), (x2, y2) = self.pending_hits[:2]
        if x1 == x2:
            self.hunt_direction = "vertical"
        elif y1 == y2:
            self.hunt_direction = "horizontal"

    def _continue_horizontal(self, board) -> tuple[int, int]:
        """
        Continue shooting left or right along a horizontal hit line.

        Args:
            board: The player's board.

        Returns:
            A tuple (x, y) or None if no valid shot exists.
        """
        hits = sorted(self.pending_hits, key=lambda p: p[0])
        left = (hits[0][0] - 1, hits[0][1])
        right = (hits[-1][0] + 1, hits[-1][1])
        return self._pick_valid(board, [left, right])

    def _continue_vertical(self, board) -> tuple[int, int]:
        """
        Continue shooting up or down along a vertical hit line.

        Args:
            board: The player's board.

        Returns:
            A tuple (x, y) or None if no valid shot exists.
        """
        hits = sorted(self.pending_hits, key=lambda p: p[1])
        up = (hits[0][0], hits[0][1] - 1)
        down = (hits[-1][0], hits[-1][1] + 1)
        return self._pick_valid(board, [up, down])

    @staticmethod
    def _pick_valid(board, candidates: list[tuple[int, int]]) -> tuple[int, int] | None:
        """
        Return the first valid shot from a list of candidates.

        Args:
            board: The player's board.
            candidates: list of (x, y) positions to test.

        Returns:
            A valid (x, y) shot or None if none are valid.
        """
        random.shuffle(candidates)
        for x, y in candidates:
            if 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS:
                if board.grid[y][x] not in [2, 3, 4]:
                    return x, y
        return None


# TODO: I am impressed by the logic you build for the enemies!
class SmartShootingStrategy(HuntShootingStrategy):
    """Advanced shooting strategy combining hunt logic with checkerboard scanning."""

    def get_next_shot(self, opponent_board) -> tuple[int, int]:
        """
        Return the next shot using hunt mode or optimized checkerboard scanning.

        Args:
            opponent_board: The player's board used to evaluate shot choices.

        Returns:
            A tuple (x, y) representing the next target cell.
        """
        if self.pending_hits:
            return super().get_next_shot(opponent_board)

        candidates = [
            (x, y)
            for y in range(GRID_ROWS)
            for x in range(GRID_COLS)
            if (x + y) % 2 == 0 and opponent_board.grid[y][x] not in [2, 3, 4]
        ]

        if candidates:
            return random.choice(candidates)

        return RandomShootingStrategy().get_next_shot(opponent_board)
