# Screen and Grid Setting
GRID_COLS = 10
GRID_ROWS = 10
BLOCK_SIZE = 40  # size of a grid cell in pixels
BOARD_SPACING = BLOCK_SIZE * 2  # distance between player and computer boards

# Colors
COLOR_BG = (0, 0, 0)
COLOR_GRID = (40, 40, 40)
COLOR_TEXT = (255, 255, 255)
COLOR_SHIP = (169, 169, 169)
COLOR_MISS = (0, 150, 255)  # Blue for Miss
COLOR_HIT = (255, 165, 0)  # Orange for Hit
COLOR_SUNK = (200, 0, 0)  # Red for sunk

# Ship config
SHIP_SIZES = {"Submarine": 1, "Frigate": 2, "Destroyer": 3, "Aircraft Carrier": 4}


FLEET = [
    "Aircraft Carrier",
    "Destroyer",
    "Frigate",
    "Submarine",
    "Submarine",
    "Submarine",
    "Submarine",
]
NUM_SUBS = 4
NUM_FRIGS = 1
NUM_DESTS = 1
NUM_ACCS = 1

# Gameplay Settings
DEFAULT_ORIENTATION = "hor"
SHIP_MARGIN = 0  # distance between ships
DEBUG_SHOW_ENEMY_SHIPS = True  # or False
# WINDOW_TITLE = "BATTLESHIP"
