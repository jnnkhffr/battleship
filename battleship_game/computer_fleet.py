import random
from battleship_game.fleet_commander import FleetManager


class ComputerFleetManager(FleetManager):
    """
    Automatically places the computer's fleet on its board
    using the same placement rules as the player.
    """

    def auto_place_fleet(self):
        """
        Randomly place all ships on the Board.
        Ensures valid placement according to Board rules.
        """
        for ship in self.ships:
            placed = False
            attempts = 0

            while not placed:
                attempts += 1

                # Random orientation
                orientation = random.choice(["hor", "ver"])

                # Random starting position
                x = random.randint(0, self.board.cols - 1)
                y = random.randint(0, self.board.rows - 1)

                # Try to place
                if self.place_ship(ship, x, y, orientation):
                    placed = True

                # Safety fallback (should never happen)
                if attempts > 500:
                    raise RuntimeError(
                        "Computer could not place a ship after many attempts."
                    )
