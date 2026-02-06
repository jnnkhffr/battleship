from battleship_game.fleet import (
    AircraftCarrier,
    Destroyer,
    Frigate,
    Submarine
)

class ShipBuilder:
    """
    Create ship objects
    """
    def create_ship(ship_type):
        """
        Returns a ship object
        """
        if ship_type == "AircraftCarrier":
            return AircraftCarrier()
        elif ship_type == "Destroyer":
            return Destroyer()
        elif ship_type == "Frigate":
            return Frigate()
        elif ship_type == "Submarine":
            return Submarine()
        else:
            raise ValueError("Ship type not recognized")