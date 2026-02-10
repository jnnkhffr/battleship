from abc import ABC, abstractmethod
from battleship_game.config import GRID_COLS, GRID_ROWS
import random


class ShootingStrategy(ABC):
    @abstractmethod
    def get_next_shot(self, opponent_board):
        pass


class RandomShootingStrategy(ShootingStrategy):
    def get_next_shot(self, opponent_board):
        while True:
            x = random.randint(0, GRID_COLS - 1)
            y = random.randint(0, GRID_ROWS - 1)

            if opponent_board.grid[y][x] not in [2, 3, 4]:
                return x, y


class HuntShootingStrategy(ShootingStrategy):
    def get_next_shot(self, opponent_board):
        # First: try adjacent to previous hits
        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                if opponent_board.grid[y][x] == 3:  # hit
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS:
                            if opponent_board.grid[ny][nx] not in [2, 3, 4]:
                                return nx, ny

        # Fallback to random
        return RandomShootingStrategy().get_next_shot(opponent_board)


class SmartShootingStrategy(ShootingStrategy):
    def get_next_shot(self, opponent_board):
        # Hunt first
        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                if opponent_board.grid[y][x] == 3:
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS:
                            if opponent_board.grid[ny][nx] not in [2, 3, 4]:
                                return nx, ny

        # Checkerboard search
        candidates = [
            (x, y)
            for y in range(GRID_ROWS)
            for x in range(GRID_COLS)
            if (x + y) % 2 == 0 and opponent_board.grid[y][x] not in [2, 3, 4]
        ]

        if candidates:
            return random.choice(candidates)

        # Final fallback
        return RandomShootingStrategy().get_next_shot(opponent_board)
