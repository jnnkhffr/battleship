
#Board Conifg.
GRID_COLS = 10
GRID_ROWS = 10

BLOCK_SIZE = 40  # size of a grid cell

BOARD_SPACING = BLOCK_SIZE * 2 #distance between two boards

#Colors
COLOR_BG: tuple[int, int, int] = (0, 0, 0)
COLOR_GRID: tuple[int, int, int] = (40, 40, 40)
COLOR_SHIP: tuple[int, int, int] = (169, 169, 169)

#Ship config.
SUB_SIZE = 1
FRIG_SIZE = 2
DEST_SIZE = 3
ACC_SIZE = 4

NUM_SUBS = 4
NUM_FRIGS = 1
NUM_DESTS = 1
NUM_ACCS = 1

#GAmeplay Settings
DEFAULT_ORIENTATION = "hor"
SHIP_MARGIN = 1 #distance between ships
