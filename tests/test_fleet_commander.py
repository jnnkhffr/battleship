"""
Tests for the FleetManager.
"""

import pytest


class TestFleetManagerInitialization:
    """Tests for FleetManager initialization."""

    # TODO: typing
    def test_fleet_manager_creates_ships(self, fleet_manager):
        """FleetManager should create all ships."""
        # According to config: 4 Submarines, 1 Frigate, 1 Destroyer, 1 AircraftCarrier
        assert len(fleet_manager.ships) == 7

    def test_fleet_manager_creates_correct_ship_types(self, fleet_manager):
        """FleetManager should create correct ship types."""
        ship_names = [ship.name for ship in fleet_manager.ships]

        assert ship_names.count("Aircraft Carrier") == 1
        assert ship_names.count("Destroyer") == 1
        assert ship_names.count("Frigate") == 1
        assert ship_names.count("Submarine") == 4


class TestShipPlacement:
    """Tests for ship placement by FleetManager."""

    def test_place_ship_returns_true_on_success(self, fleet_manager):
        """place_ship should return True on successful placement."""
        ship = fleet_manager.ships[0]
        result = fleet_manager.place_ship(ship, x=0, y=0, orientation="hor")
        assert result is True

    def test_place_ship_returns_false_on_failure(self, fleet_manager):
        """place_ship should return False on invalid placement."""
        ship = fleet_manager.ships[0]
        # Try placing outside the board
        result = fleet_manager.place_ship(ship, x=10, y=10, orientation="hor")
        assert result is False

    def test_place_ship_sets_ship_position(self, fleet_manager):
        """place_ship should store the ship position."""
        ship = fleet_manager.ships[0]
        fleet_manager.place_ship(ship, x=2, y=3, orientation="hor")

        assert ship.position == (2, 3)
        assert ship.orientation == "hor"

    def test_all_ships_placed_returns_false_initially(self, fleet_manager):
        """all_ships_placed should return False when no ships are placed."""
        assert fleet_manager.all_ships_placed() is False

    def test_all_ships_placed_returns_true_when_done(self, fleet_manager):
        """all_ships_placed should return True when all ships are placed."""
        # Place all ships intelligently on the board
        positions = [
            (0, 0, "hor"),
            (0, 2, "hor"),
            (0, 4, "hor"),
            (0, 6, "hor"),
            (5, 0, "hor"),
            (5, 2, "hor"),
            (5, 4, "hor"),
        ]

        for ship, (x, y, orientation) in zip(fleet_manager.ships, positions):
            result = fleet_manager.place_ship(ship, x=x, y=y, orientation=orientation)
            assert result is True, f"Could not place {ship.name} at ({x},{y})"

        assert fleet_manager.all_ships_placed() is True


class TestReceiveShot:
    """Tests for shot handling."""

    def test_receive_shot_returns_none_on_miss(self, fleet_manager):
        """receive_shot should return None on a miss."""
        ship = fleet_manager.ships[0]
        fleet_manager.place_ship(ship, x=5, y=5, orientation="hor")

        result = fleet_manager.receive_shot(x=0, y=0)
        assert result is None

    def test_receive_shot_returns_ship_on_hit(self, fleet_manager):
        """receive_shot should return the ship on a hit."""
        ship = fleet_manager.ships[0]
        fleet_manager.place_ship(ship, x=5, y=5, orientation="hor")

        result = fleet_manager.receive_shot(x=5, y=5)
        assert result == ship

    def test_receive_shot_registers_hit_on_ship(self, fleet_manager):
        """receive_shot should register a hit on the ship."""
        ship = fleet_manager.ships[0]
        fleet_manager.place_ship(ship, x=5, y=5, orientation="hor")

        fleet_manager.receive_shot(x=5, y=5)
        assert ship.hits == 1

    @pytest.mark.parametrize(
        "x,y,expected_hit",
        [
            (2, 3, True),  # Start of ship
            (3, 3, True),  # Middle
            (4, 3, True),  # End
            (1, 3, False),  # Left of ship
            (5, 3, False),  # Right of ship
            (2, 2, False),  # Above
            (2, 4, False),  # Below
        ],
    )
    def test_receive_shot_detects_hits_correctly(
        self, fleet_manager, x, y, expected_hit
    ):
        """receive_shot should correctly detect hits."""
        # Place size-3 ship horizontally at (2,3)
        ship = None
        for s in fleet_manager.ships:
            if s.size == 3:
                ship = s
                break

        fleet_manager.place_ship(ship, x=2, y=3, orientation="hor")

        result = fleet_manager.receive_shot(x, y)

        if expected_hit:
            assert result == ship
        else:
            assert result is None


class TestFleetDefeat:
    """Tests for fleet defeat."""

    def test_is_defeated_returns_false_initially(self, fleet_manager):
        """is_defeated should return False initially."""
        y = 0
        for ship in fleet_manager.ships:
            fleet_manager.place_ship(ship, x=0, y=y, orientation="hor")
            y += 2

        assert fleet_manager.is_defeated() is False

    def test_is_defeated_returns_true_when_all_ships_sunk(self, fleet_manager):
        """is_defeated should return True when all ships are sunk."""
        y = 0
        for ship in fleet_manager.ships:
            fleet_manager.place_ship(ship, x=0, y=y, orientation="hor")

            # Sink the ship
            for _ in range(ship.size):
                ship.register_hits()

            y += 2

        assert fleet_manager.is_defeated() is True
