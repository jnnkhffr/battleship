from abc import ABC, abstractmethod
from battleship_game.config import GRID_COLS, GRID_ROWS
import random


class ShootingStrategy(ABC):
    @abstractmethod
    def get_next_shot(self, opponent_board):
        pass

    def register_shot_result(self, x, y, hit, sunk):
        pass


class RandomShootingStrategy(ShootingStrategy):
    def get_next_shot(self, opponent_board):
        while True:
            x = random.randint(0, GRID_COLS - 1)
            y = random.randint(0, GRID_ROWS - 1)

            if opponent_board.grid[y][x] not in [2, 3, 4]:
                return x, y


class HuntShootingStrategy(ShootingStrategy):
    def __init__(self):
        self.pending_hits = []
        self.hunt_direction = None

    def get_next_shot(self, opponent_board):
        # Falls wir Treffer haben → Target Mode
        if self.pending_hits:
            return self._target_mode(opponent_board)

        # Sonst: Treffer suchen und merken
        self._scan_for_hits(opponent_board)

        if self.pending_hits:
            return self._target_mode(opponent_board)

        # Fallback: Random
        return RandomShootingStrategy().get_next_shot(opponent_board)

    def register_shot_result(self, x, y, hit, sunk):
        if hit:
            self.pending_hits.append((x, y))

        if sunk:
            self.pending_hits.clear()
            self.hunt_direction = None

    def _scan_for_hits(self, board):
        self.pending_hits.clear()
        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                if board.grid[y][x] == 3:
                    self.pending_hits.append((x, y))

    def _target_mode(self, board):
        # 1 Treffer → Nachbarn probieren
        if len(self.pending_hits) == 1:
            x, y = self.pending_hits[0]
            candidates = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
            shot = self._pick_valid(board, candidates)
            if shot:
                return shot

        # Richtung bestimmen
        if self.hunt_direction is None:
            self._determine_direction()

        # Horizontal weiterschießen
        if self.hunt_direction == "horizontal":
            return self._continue_horizontal(board)

        # Vertikal weiterschießen
        if self.hunt_direction == "vertical":
            return self._continue_vertical(board)

        # Fallback
        return RandomShootingStrategy().get_next_shot(board)

    def _determine_direction(self):
        if len(self.pending_hits) < 2:
            return
        (x1, y1), (x2, y2) = self.pending_hits[:2]
        if x1 == x2:
            self.hunt_direction = "vertical"
        elif y1 == y2:
            self.hunt_direction = "horizontal"

    def _continue_horizontal(self, board):
        hits = sorted(self.pending_hits, key=lambda p: p[0])
        left = (hits[0][0] - 1, hits[0][1])
        right = (hits[-1][0] + 1, hits[-1][1])
        return self._pick_valid(board, [left, right])

    def _continue_vertical(self, board):
        hits = sorted(self.pending_hits, key=lambda p: p[1])
        up = (hits[0][0], hits[0][1] - 1)
        down = (hits[-1][0], hits[-1][1] + 1)
        return self._pick_valid(board, [up, down])

    def _pick_valid(self, board, candidates):
        random.shuffle(candidates)
        for x, y in candidates:
            if 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS:
                if board.grid[y][x] not in [2, 3, 4]:
                    return x, y
        return None



class SmartShootingStrategy(HuntShootingStrategy):

    def get_next_shot(self, opponent_board):
        if self.pending_hits:
            return super().get_next_shot(opponent_board)

        candidates = [
            (x, y)
            for y in range(GRID_ROWS)
            for x in range(GRID_COLS)
            if (x + y) % 2 == 0 and opponent_board.grid[y][x] not in [2, 3, 4]
        ]

        if candidates:
            return random.choice(candidates)

        # Fallback
        return RandomShootingStrategy().get_next_shot(opponent_board)
