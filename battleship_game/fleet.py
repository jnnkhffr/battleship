from battleship_game.config import SUB_SIZE, FRIG_SIZE, DEST_SIZE, ACC_SIZE


class Ship:
    """
    Base class for all ship types.
    Stores size, position and orientation and hit tracking.
    """

    def __init__(self, size: int, position: tuple | None, orientation: str | None):
        self.size = size
        self.position = position
        self.orientation = orientation
        self.hits = 0

    def register_hits(self):
        "Increase hit counter when this ship is hit."
        self.hits += 1

    def is_sunk(self):
        """Return true if the ship has been hit as many times as its size."""
        return self.hits >= self.size


# All ships in different classes


class Submarine(Ship):
    def __init__(self, position=None, orientation=None):
        super().__init__(SUB_SIZE, position, orientation)
        self.name = "Submarine"


class Frigate(Ship):
    def __init__(self, position=None, orientation=None):
        super().__init__(FRIG_SIZE, position, orientation)
        self.name = "Frigate"


class Destroyer(Ship):
    def __init__(self, position=None, orientation=None):
        super().__init__(DEST_SIZE, position, orientation)
        self.name = "Destroyer"


class AircraftCarrier(Ship):
    def __init__(self, position=None, orientation=None):
        super().__init__(ACC_SIZE, position, orientation)
        self.name = "Aircraft Carrier"
