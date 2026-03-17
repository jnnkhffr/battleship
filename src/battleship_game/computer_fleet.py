"""Initializes the computer fleet."""

from battleship_game.ai_shooting import ShootingStrategy
from battleship_game.config import GRID_COLS, GRID_ROWS
from battleship_game.fleet_commander import FleetManager
import random


class ComputerFleetManager(FleetManager):
    """
    Manage the computer fleet (ENEMY).
    Takes logic from FleetManager and adds the enemy logic.
    """

    def __init__(self, board, shooting_strategy: ShootingStrategy) -> None:
        """
        Initialize the computer fleet manager with a board and AI shooting strategy.

        Args:
            board: The enemy's game board.
            shooting_strategy: Strategy object that determines how the AI selects shots.
        """
        super().__init__(board)
        self.strategy = shooting_strategy

    def auto_place_fleet(self) -> None:
        """
        Randomly place all enemy ships on the board until all are validly positioned.

        Args:
            None.

        Returns:
            None. Ships are placed directly onto the enemy board.
        """
        for ship in self.ships:
            placed = False
            while not placed:
                # Random placement and orientation
                x = random.randint(0, GRID_COLS - 1)
                y = random.randint(0, GRID_ROWS - 1)
                orientation = random.choice(["hor", "ver"])

                # Place the enemy ship
                if self.place_ship(ship, x, y, orientation):
                    placed = True

    def get_next_shot(self, opponent_board) -> tuple[int, int]:
        """
        Determine the next shot coordinates using the assigned shooting strategy.

        Args:
            opponent_board: The player's board used to evaluate shot decisions.

        Returns:
            A tuple (x, y) representing the next target cell.
        """
        return self.strategy.get_next_shot(opponent_board)
