from battleship_game.fleet import (
    Submarine,
    Frigate,
    Destroyer,
    AircraftCarrier,
)
from battleship_game.config import (
    NUM_SUBS,
    NUM_FRIGS,
    NUM_DESTS,
    NUM_ACCS,
)


class FleetManager:
    """
    Manages the player's fleet.

    Responsibilities:
    - Create all ships according to configuration
    - Store ship objects
    - Handle placement attempts on the board
    """

    def __init__(self, board):
        """
        Initialize the fleet manager.

        Args:
            board: The player's Board instance where ships will be placed.
        """
        self.board = board
        self.ships = []

        self.create_fleet()


    def create_fleet(self):
        """
        Create the player's fleet based on configuration values.

        Ships are created in recommended placement order:
        largest → smallest.
        """

        # Aircraft carriers
        for _ in range(NUM_ACCS):
            self.ships.append(AircraftCarrier())

        # Destroyers
        for _ in range(NUM_DESTS):
            self.ships.append(Destroyer())

        # Frigates
        for _ in range(NUM_FRIGS):
            self.ships.append(Frigate())

        # Submarines
        for _ in range(NUM_SUBS):
            self.ships.append(Submarine())


    def place_ship(self, ship, x, y, orientation):
        """
        Attempt to place a ship on the board.

        Args:
            ship: Ship object to place.
            x: Column index.
            y: Row index.
            orientation: "hor" or "ver".

        Returns:
            True if placement succeeded, False otherwise.
        """
        if self.board.can_place_ship(x, y, ship.size, orientation):
            ship.position = (x, y)
            ship.orientation = orientation
            self.board.place_ship(x, y, ship.size, orientation)
            return True
        return False


    def all_ships_placed(self):
        """
        Check whether all ships have been assigned a position.

        Returns:
            True if all ships are placed, False otherwise.
        """
        return all(ship.position is not None for ship in self.ships)
