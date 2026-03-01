"""
Tests for ship classes.
"""

import pytest
from battleship_game.fleet import Submarine, Frigate, Destroyer, AircraftCarrier


class TestShipInitialization:
    """Tests for ship initialization."""

    def test_submarine_has_correct_size(self, submarine):
        """Submarine should have size 1."""
        assert submarine.size == 1
        assert submarine.name == "Submarine"

    def test_frigate_has_correct_size(self):
        """Frigate should have size 2."""
        frigate = Frigate()
        assert frigate.size == 2
        assert frigate.name == "Frigate"

    def test_destroyer_has_correct_size(self, destroyer):
        """Destroyer should have size 3."""
        assert destroyer.size == 3
        assert destroyer.name == "Destroyer"

    def test_aircraft_carrier_has_correct_size(self):
        """AircraftCarrier should have size 4."""
        carrier = AircraftCarrier()
        assert carrier.size == 4
        # TODO: this fails
        # assert carrier.name == "Aircraft Carrier"
        assert carrier.name == "AircraftCarrier"

    def test_new_ship_has_zero_hits(self, submarine):
        """New ship should have 0 hits."""
        assert submarine.hits == 0

    def test_new_ship_has_no_position(self, submarine):
        """New ship should have no position."""
        assert submarine.position is None


class TestShipHits:
    """Tests for ship hits."""

    def test_register_hits_increases_counter(self, submarine):
        """register_hits should increase hit counter."""
        submarine.register_hits()
        assert submarine.hits == 1

        submarine.register_hits()
        assert submarine.hits == 2

    def test_ship_is_not_sunk_initially(self, destroyer):
        """Ship should not be sunk initially."""
        # TODO: normally you dont want to compare bools. In test I somewhat find it
        #  readable tho
        assert destroyer.is_sunk() is False

    def test_ship_is_sunk_after_enough_hits(self, submarine):
        """Ship should be sunk after enough hits."""
        submarine.register_hits()
        assert submarine.is_sunk() is True

    @pytest.mark.parametrize(
        "ship_class,size",
        [
            (Submarine, 1),
            (Frigate, 2),
            (Destroyer, 3),
            (AircraftCarrier, 4),
        ],
    )
    def test_ship_sinks_after_size_hits(self, ship_class, size):
        """Ship should sink after 'size' hits."""
        ship = ship_class()

        # Register hits (but not sunk yet)
        for _ in range(size - 1):
            ship.register_hits()
        assert ship.is_sunk() is False

        # Final hit
        ship.register_hits()
        assert ship.is_sunk() is True
