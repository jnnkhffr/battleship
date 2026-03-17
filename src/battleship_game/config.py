import os

# Board Config.
GRID_COLS = 10
GRID_ROWS = 10
BLOCK_SIZE = 40  # size of a grid cell in pixel
BOARD_SPACING = BLOCK_SIZE * 2  # distance between two boards
WINDOW_WIDTH = GRID_COLS * BLOCK_SIZE * 2 + BOARD_SPACING
WINDOW_HEIGHT = GRID_ROWS * BLOCK_SIZE
DURATION = 3000
DELAY = 600  # millisec
FPS = 60


# Colors
# TODO: One could use a class here (for more structure and easier importing)
class Color:
    BG = (0, 0, 0)
    OVERLAY = (0, 0, 0)
    GRID = (40, 40, 40)
    SHIP = (169, 169, 169)
    MISS = (0, 150, 255)
    HIT = (255, 165, 0)
    SUNK = (255, 0, 0)
    MESSAGE = (0, 255, 0)
    PREVIEW = (255, 88, 80)
    TEXT = (255, 255, 255)
    MESSAGE_FIRING = (0, 0, 200)
    FILL = (255, 0, 0, 255)


OVERLAY_ALPHA = 128

# Ship placement
ALPHA_PREVIEW = 128

# Ship config.
SUB_SIZE = 1
FRIG_SIZE = 2
DEST_SIZE = 3
ACC_SIZE = 4

NUM_SUBS = 4
NUM_FRIGS = 1
NUM_DESTS = 1
NUM_ACCS = 1

# For Screens
FONT_TITLE = 72
FONT_SUBTITLE = 32
FONT_BUTTON = 48
FONT_GAMEOVER = 48

BUTTON_WIDTH_FACTOR = 0.35
BUTTON_HEIGHT_FACTOR = 0.08
BUTTON_REPLAY_Y = 0.55
BUTTON_MENU_Y = 0.68

# Gameplay Settings
DEFAULT_ORIENTATION = "hor"
SHIP_MARGIN: int = 1  # distance between ships
DEBUG_SHOW_ENEMY_SHIPS = True  # or False

# TODO: Constants should be allcaps
# Absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Assets path relative to file
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Sound paths using assets directory
THEME_SOUND = os.path.join(ASSETS_DIR, "sounds", "theme.mp3")
HIT_SOUND = os.path.join(ASSETS_DIR, "sounds", "hit.wav")
SUNK_SOUND = os.path.join(ASSETS_DIR, "sounds", "sunk.wav")
MISS_SOUND = os.path.join(ASSETS_DIR, "sounds", "miss.wav")

# Volume levels
HIT_SOUND_VOL = 0.1
SUNK_SOUND_VOL = 0.3
MISS_SOUND_VOL = 0.05
VOLUME = 0.1


# Tokens
HIT_TOKEN = os.path.join(ASSETS_DIR, "images", "tokens", "greentoken.png")
MISS_TOKEN = os.path.join(ASSETS_DIR, "images", "tokens", "bluetoken.png")
SUNK_TOKEN = os.path.join(ASSETS_DIR, "images", "tokens", "redtoken.png")

# Images
MAIN_BG = os.path.join(ASSETS_DIR, "images", "background", "battleship.jpg")
PLAYER_GRID = os.path.join(ASSETS_DIR, "images", "grids", "player_grid.png")
ENEMY_GRID = os.path.join(ASSETS_DIR, "images", "grids", "enemy_grid.png")
# Ship Configuration: Size, Image Path
SHIP_DATA = {
    "AircraftCarrier": (
        4,
        os.path.join(ASSETS_DIR, "images", "ships", "AircraftCarrier.png"),
    ),
    "Destroyer": (3, os.path.join(ASSETS_DIR, "images", "ships", "Destroyer.png")),
    "Frigate": (2, os.path.join(ASSETS_DIR, "images", "ships", "Frigate.png")),
    "Submarine": (1, os.path.join(ASSETS_DIR, "images", "ships", "Submarine.png")),
}
