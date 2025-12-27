import random
from battleship_game.ship import Ship
from battleship_game.config import FLEET


class Fleet:
    """
    Manages the player's fleet.

    Responsibilities:
    - Create all ships according to configuration
    - Store ship objects
    - Handle placement attempts on the board
    - Hit Logic
    """

    def __init__(self, board):
        """
        Initialize the fleet manager.

        Args:
            board: The player's Board instance where ships will be placed.
        """
        self.board = board
        self.ships: list[Ship] = []
        self.create_fleet()

    def create_fleet(self) -> None:
        """
        Create the player's fleet based on configuration values.

        Ships are created in recommended placement order:
        largest → smallest.
        """
        for ship_name in FLEET:
            new_ship = Ship(ship_name)
            self.ships.append(new_ship)

    def auto_place_fleet(self):
        """
        Randomly place all ships on the Board.
        Ensures valid placement according to Board rules.
        """
        for ship in self.ships:
            placed = False
            attempts = 0

            while not placed:
                attempts += 1

                # Random orientation
                orientation = random.choice(["hor", "ver"])

                # Random starting position
                x = random.randint(0, self.board.cols - 1)
                y = random.randint(0, self.board.rows - 1)

                # Try to place
                if self.place_ship(ship, x, y, orientation):
                    placed = True

                # Safety fallback (should never happen)
                if attempts > 500:
                    raise RuntimeError(
                        "Computer could not place a ship after many attempts."
                    )

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
        if self.board.can_place_ship(ship, x, y, orientation):
            # Update the ship position
            ship.position = (x, y)
            ship.orientation = orientation

            # Update the board
            self.board.place_ship(ship, x, y)
            return True

        return False

    def shot(self, x: int, y: int):
        """
        Checks if a shot at (x, y) hits any ship.
        Returns the Ship object if Hit, None if Miss.
        """
        for ship in self.ships:
            if ship.position is None:
                continue  # Skip unplaced ships

            sx, sy = ship.position
            dx = 1 if ship.orientation == "hor" else 0
            dy = 1 if ship.orientation == "ver" else 0

            # Check if coordinates match any ship segment
            for i in range(ship.size):
                if x == (sx + dx * i) and y == (sy + dy * i):
                    ship.hit()
                    return ship
        return None

    def is_defeated(self) -> bool:
        """True if all ships are sunk."""
        return all(ship.is_sunk for ship in self.ships)

    def __iter__(self):
        return iter(self.ships)
