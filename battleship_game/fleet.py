"""Initializes the fleet."""
from __future__ import annotations
from battleship_game.config import SUB_SIZE, FRIG_SIZE, DEST_SIZE, ACC_SIZE


class Ship:
    """
    Base class for all ship types.
    Stores size, position and orientation and hit tracking.
    """

    def __init__(self, size: int, position: tuple | None, orientation: str | None):
        """
        Initialize a ship with size, position, orientation, and hit counter.

        Args:
            size: Length of the ship.
            position: Starting (x, y) grid position or None if unplaced.
            orientation: "hor" or "ver", or None if not yet set.
        """
        self.size = size
        self.position = position
        self.orientation = orientation
        self.hits = 0

    def register_hits(self):
        """Increase hit counter when this ship is hit."""
        self.hits += 1

    def is_sunk(self):
        """
        Return true if the ship has been hit as many times as its size.

        Returns:
            True if the ship is sunk, otherwise False.
        """
        return self.hits >= self.size


class Submarine(Ship):
    """Submarine ship with predefined size."""

    def __init__(self, position=None, orientation=None):
        """
        Initialize a submarine with optional position and orientation.

        Args:
            position: Starting grid position or None.
            orientation: "hor" or "ver", or None.
        """
        super().__init__(SUB_SIZE, position, orientation)
        self.name = "Submarine"


class Frigate(Ship):
    """Frigate ship with predefined size."""

    def __init__(self, position=None, orientation=None):
        """Initialize a frigate with optional position and orientation."""
        super().__init__(FRIG_SIZE, position, orientation)
        self.name = "Frigate"


class Destroyer(Ship):
    """Destroyer ship with predefined size."""

    def __init__(self, position=None, orientation=None):
        """Initialize a destroyer with optional position and orientation."""
        super().__init__(DEST_SIZE, position, orientation)
        self.name = "Destroyer"


class AircraftCarrier(Ship):
    """Aircraft Carrier with predefined size."""

    def __init__(self, position=None, orientation=None):
        """Initialize an Aircraft Carrier with optional position and orientation."""
        super().__init__(ACC_SIZE, position, orientation)
        self.name = "AircraftCarrier"
