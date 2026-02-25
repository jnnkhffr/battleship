"""
This module defines the behavior for different difficulty levels in the
Battleship game.

Available modes:
- Easy:   Pure random shooting with no memory or strategy.
- Medium: Hunt-and-target logic that attempts to finish off ships once hit.
- Hard:   Placeholder for future advanced AI (e.g., probability-based logic).
"""

import random
from config import GRID_COLS, GRID_ROWS


# easy is what we had in the computer_fleet before
class EasyAI:
    """
    AI Mode: Easy

    This AI selects random coordinates that have not been shot yet.
    It does not store any information about previous hits or misses
    and does not attempt to follow up on successful shots.

    This mode provides the lowest difficulty and is ideal for beginners.
    """

    def get_next_shot(self, board):
        """
        Selects a random, unshot coordinate on the opponent's board.

        Args:
            board: The opponent's Board instance used to check shot history.

        Returns:
            tuple[int, int]: The (x, y) coordinates of the next shot.
        """
        while True:
            x = random.randint(0, GRID_COLS - 1)
            y = random.randint(0, GRID_ROWS - 1)
            if board.grid[y][x] not in [2, 3, 4]:  # 2=hit, 3=miss, 4=sunk
                return x, y

    def register_shot_result(self, x, y, hit, sunk):
        """
        Processes the result of a shot.

        Easy does not store or react to shot results. This method exists
        only to maintain a consistent interface across AI modes.

        Args:
            x (int): X-coordinate of the shot.
            y (int): Y-coordinate of the shot.
            hit (bool): Whether the shot hit a ship.
            sunk (bool): Whether the shot sank a ship.
        """
        pass


class MediumAI:
    """
    AI Mode: Medium

    Implements a classic "hunt-and-target" strategy:
    - When no hits are pending, the AI behaves like EasyAI (random shots).
    - When a ship is hit, the AI switches to target mode and probes
      adjacent tiles to determine the ship's orientation.
    - Once the orientation is known, the AI continues firing along the line
      until the ship is sunk.

    This mode provides a noticeable challenge without being unfair.
    """

    def __init__(self):
        """
        Initializes internal state used for tracking ongoing ship hunts.
        """
        self.pending_hits = []  # Coordinates of hits on ships not yet sunk
        self.hunt_direction = None  # "horizontal" or "vertical"

    def get_next_shot(self, board):
        """
        Determines the next shot based on current AI state.

        If the AI has active hits, it enters target mode. Otherwise,
        it falls back to random shooting.

        Args:
            board: The opponent's Board instance.

        Returns:
            tuple[int, int]: The (x, y) coordinates of the next shot.
        """
        if self.pending_hits:
            return self._target_mode(board)

        return EasyAI().get_next_shot(board)

    def register_shot_result(self, x, y, hit, sunk):
        """
        Updates the AI's internal state based on the result of a shot.

        Args:
            x (int): X-coordinate of the shot.
            y (int): Y-coordinate of the shot.
            hit (bool): Whether the shot hit a ship.
            sunk (bool): Whether the shot sank the ship that was hit.
        """
        if hit:
            self.pending_hits.append((x, y))

            # If the ship is sunk, reset hunt state
            if sunk:
                self.pending_hits.clear()
                self.hunt_direction = None

    def _target_mode(self, board):
        """
        Executes targeted shooting around known hit coordinates.

        Returns:
            tuple[int, int]: The next targeted shot.
        """
        # Only one hit → probe neighbors
        if len(self.pending_hits) == 1:
            x, y = self.pending_hits[0]
            candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            shot = self._pick_valid(board, candidates)
            if shot:
                return shot

        # Determine orientation if not known
        if self.hunt_direction is None:
            self._determine_direction()

        # Continue along the detected orientation
        if self.hunt_direction == "horizontal":
            return self._continue_horizontal(board)

        if self.hunt_direction == "vertical":
            return self._continue_vertical(board)

        # Fallback to random if something unexpected happens
        return EasyAI().get_next_shot(board)

    def _pick_valid(self, board, candidates):
        """
        Filters and returns the first valid shot from a list of candidates.

        Args:
            board: Opponent's board.
            candidates (list[tuple[int, int]]): Potential shot coordinates.

        Returns:
            tuple[int, int] | None: A valid shot coordinate or None if none apply.
        """
        random.shuffle(candidates)
        for x, y in candidates:
            if 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS:
                if board.grid[y][x] not in [2, 3, 4]:
                    return x, y
        return None

    def _determine_direction(self):
        """
        Determines whether the ship being targeted is horizontal or vertical
        based on the first two hit coordinates.
        """
        if len(self.pending_hits) < 2:
            return

        (x1, y1), (x2, y2) = self.pending_hits[:2]

        if x1 == x2:
            self.hunt_direction = "vertical"
        elif y1 == y2:
            self.hunt_direction = "horizontal"

    def _continue_horizontal(self, board):
        """
        Continues firing left or right along a horizontal ship.

        Returns:
            tuple[int, int]: The next shot coordinate.
        """
        hits = sorted(self.pending_hits, key=lambda p: p[0])
        left = (hits[0][0] - 1, hits[0][1])
        right = (hits[-1][0] + 1, hits[-1][1])
        return self._pick_valid(board, [left, right])

    def _continue_vertical(self, board):
        """
        Continues firing up or down along a vertical ship.

        Returns:
            tuple[int, int]: The next shot coordinate.
        """
        hits = sorted(self.pending_hits, key=lambda p: p[1])
        up = (hits[0][0], hits[0][1] - 1)
        down = (hits[-1][0], hits[-1][1] + 1)
        return self._pick_valid(board, [up, down])


class HardAI:
    """
    AI Mode: Hard

    Placeholder for a future advanced AI implementation.
    Currently behaves identically to EasyAI.
    """

    def get_next_shot(self, board):
        return EasyAI().get_next_shot(board)

    def register_shot_result(self, x, y, hit, sunk):
        pass
