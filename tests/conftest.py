"""
Fixtures for Battleship tests.
These can be used in all tests.
"""

import pytest
from battleship_game import Board
from battleship_game.fleet import Submarine, Destroyer
from battleship_game import FleetManager


# TODO: love the usage of fixtures!
@pytest.fixture
def empty_board():
    """Creates an empty 10x10 game board."""
    # TODO: the tests are failing the latest version (the ran before)
    #  fix the test - Obviously, `grid_image_path` is not an optional parameter
    return Board()


@pytest.fixture
def board_with_ship():
    """Creates a board with a placed ship."""
    board = Board()
    board.place_ship(x=2, y=3, size=3, orientation="hor")
    return board


@pytest.fixture
def submarine():
    """Creates a Submarine object."""
    return Submarine()


@pytest.fixture
def destroyer():
    """Creates a Destroyer object."""
    return Destroyer()


@pytest.fixture
def fleet_manager(empty_board):
    """Creates a FleetManager with an empty board."""
    return FleetManager(empty_board)
