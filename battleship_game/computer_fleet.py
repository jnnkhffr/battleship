from battleship_game.config import GRID_COLS, GRID_ROWS
from battleship_game.fleet_commander import FleetManager
import random


class ComputerFleetManager(FleetManager):
    """
    Manage the computer fleet (ENEMY).
    Takes logic from FleetManager and adds the enemy logic.
    """

    def __init__(self, board, shooting_strategy):
        super().__init__(board)
        self.shooting_strategy = shooting_strategy

    def auto_place_fleet(self):
        """
        Randomly place all enemy ships on board.
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

    def get_next_shot(self, opponent_board):
        return self.shooting_strategy.get_next_shot(opponent_board)
