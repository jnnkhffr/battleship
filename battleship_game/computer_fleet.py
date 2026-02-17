from battleship_game.config import GRID_COLS, GRID_ROWS
from battleship_game.fleet_commander import FleetManager
import random
from game_mode import EasyAI, MediumAI, HardAI


class ComputerFleetManager(FleetManager):
    """
    Manage the computer fleet (ENEMY).
    Takes logic from FleetManager and adds the enemy logic.
    """

    def __init__(self, board, difficulty="Easy"):
        """ Initialize the computer fleet and select the appropriate AI mode.

        Args:
            board: The Board instance representing the enemy's grid.
            difficulty (str): One of "Easy", "Medium", "Hard".
        """

        super().__init__(board)
        self.board = board

        # Selcet AI mode
        if difficulty == "Easy":
            self.ai = EasyAI()
        elif difficulty == "Medium":
            self.ai = MediumAI()
        else:
            self.ai = HardAI()

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
        """
        Delegates shot selection to the active AI mode.

        Args:
            opponent_board: The player's board.

        Returns:
            (x, y): Coordinates of the next shot.
        """
        return self.ai.get_next_shot(opponent_board)

    def register_shot_result(self, x, y, hit, sunk):
        """
        Passes the result of a shot back to the AI so it can update its strategy.

        Args:
            x (int): X-coordinate of the shot.
            y (int): Y-coordinate of the shot.
            hit (bool): Whether the shot hit a ship.
            sunk (bool): Whether the ship was sunk.
        """
        self.ai.register_shot_result(x, y, hit, sunk)

