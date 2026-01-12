from battleship_game.config import SHIP_SIZES


class Ship:
    """
    Represents a single ship in the Battleship game.
    This class maintains the state of ship.
    """

    def __init__(self, name):
        """
        Initialize a ship.
        Args:
            name (str): Specific type of ship
        """
        self.name = name
        self.size = SHIP_SIZES[name]

        # Tracking state
        self.hits = 0  # damage
        self.position = None  # (x,y) tuple after placement
        self.orientation = None  # "hor" or "ver" after placement

    def hit(self):
        """
        Increases the hit of the ship by one.
        """
        self.hits += 1

    def is_sunk(self):
        """
        Returns if the ship is destroyed if hits are greater or equal to size of shipschange
        """
        return self.hits >= self.size
