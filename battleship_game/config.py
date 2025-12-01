# Grid Configs
GRID_COLS = 10
GRID_ROWS = 10
BLOCK_SIZE = 40  # size of a grid cell
COLOR_BG: tuple[int, int, int] = (0, 0, 0)
COLOR_GRID: tuple[int, int, int] = (40, 40, 40)

# Ships form factor config
SHIP_DATA = {"Aircraft Carrier": 4, "Destroyer": 3, "Frigate": 2, "Submarine": 1}

# Fleet config
FLEET_DATA = [
    "Aircraft Carrier",
    "Destroyer",
    "Frigate",
    "Submarine",
    "Submarine",
    "Submarine",
    "Submarine",
]

SUB_SIZE = 1
FRIG_SIZE = 2
DEST_SIZE = 3
ACC_SIZE = 4
