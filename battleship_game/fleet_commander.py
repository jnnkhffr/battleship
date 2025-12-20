from battleship_game.fleet import submarine, frigate, destroyer, aircraft_carrier
from battleship_game.config import SUB_SIZE, FRIG_SIZE, DEST_SIZE, ACC_SIZE


class FleetManager:
    """
    The fleet commander or manager manages the player's fleet.
    It is the shipyard and produces the ships and determines the formation
    in which they must be arranged on the sea (board).
    """

    def __init__(self, board):
        self.board = board
        self.ships = []

        # create fleet
        self.create_fleet()

    def create_fleet(self):
        """Produces the ships of the fleet."""

        # 1 aircraft carrier
        self.ships.append(aircraft_carrier(ACC_SIZE, None, None))

        # 1 destroyer
        self.ships.append(destroyer(DEST_SIZE, None, None))

        # 1 frigate
        self.ships.append(frigate(FRIG_SIZE, None, None))

        # 4 Subs
        for _ in range(4):
            self.ships.append(submarine(SUB_SIZE, None, None))


    def place_ship(self, ship, x, y, orientation):
        """
        Tries to places ships on board.
        If it was successful it gives True back.
        """
        if self.board.can_place_ship(x, y, ship.size, orientation):
            ship.position = (x, y)
            ship.orientation = orientation
            self.board.place_ship(x, y, ship.size, orientation)
            return True
        return False

    def all_ships_placed(self):
        """Checks if all ships have a position."""
        return all(ship.position is not None for ship in self.ships)
