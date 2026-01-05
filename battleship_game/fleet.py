from battleship_game.config import SUB_SIZE, FRIG_SIZE, DEST_SIZE, ACC_SIZE


class ship:
    """
    Base class for all ship types.
    Stores size, position and orientation.
    """

    def __init__(self, size: int, position: tuple | None, orientation: str | None):
        self.size = size
        self.position = position
        self.orientation = orientation


# All ships in different classes


class Submarine(ship):
    def __init__(self, position=None, orientation=None):
        super().__init__(SUB_SIZE, position, orientation)


class Frigate(ship):
    def __init__(self, position=None, orientation=None):
        super().__init__(FRIG_SIZE, position, orientation)


class Destroyer(ship):
    def __init__(self, position=None, orientation=None):
        super().__init__(DEST_SIZE, position, orientation)


class AircraftCarrier(ship):
    def __init__(self, position=None, orientation=None):
        super().__init__(ACC_SIZE, position, orientation)
