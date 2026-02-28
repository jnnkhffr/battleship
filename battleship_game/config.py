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
COLOR_BG: tuple[int, int, int] = (0, 0, 0)
COLOR_OVERLAY: tuple[int, int, int] = (0, 0, 0)
COLOR_GRID: tuple[int, int, int] = (40, 40, 40)
COLOR_SHIP: tuple[int, int, int] = (169, 169, 169)
COLOR_MISS: tuple[int, int, int] = (0, 150, 255)  # Blue for Miss
COLOR_HIT: tuple[int, int, int] = (255, 165, 0)  # Orange for Hit
COLOR_SUNK: tuple[int, int, int] = (255, 0, 0)  # Red for sunk
COLOR_MESSAGE: tuple[int, int, int] = (0, 255, 0)
COLOR_PREVIEW: tuple[int, int, int] = (255, 80, 80)
COLOR_TEXT: tuple[int, int, int] = (255, 255, 255)
COLOR_MESSAGE_FIRING: tuple[int, int, int] = (0, 0, 200)

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
DEBUG_SHOW_ENEMY_SHIPS = False  # or False

# Sounds
Theme = "assets/sounds/theme.mp3"
hit = "assets/sounds/hit.wav"
sunk = "assets/sounds/sunk.wav"
miss = "assets/sounds/miss.wav"

# Tokens
hit_token = "assets/images/tokens/greentoken.png"
miss_token = "assets/images/tokens/bluetoken.png"
sunk_token = "assets/images/tokens/redtoken.png"

# Images
main_bg = "assets/images/background/Battleship.jpg"
player_grid = "assets/images/grids/player_grid.png"
enemy_grid = "assets/images/grids/enemy_grid.png"

# Ship Configuration: Size, Image Path
SHIP_DATA = {
    "AircraftCarrier": (4, "assets/images/ships/AircraftCarrier.png"),
    "Destroyer": (3, "assets/images/ships/Destroyer.png"),
    "Frigate": (2, "assets/images/ships/Frigate.png"),
    "Submarine": (1, "assets/images/ships/Submarine.png"),
}
