from battleship_game.game import Game
from battleship_game.start_screen import StartScreen
from battleship_game.config import GRID_COLS, GRID_ROWS, BLOCK_SIZE, BOARD_SPACING


def main():
    # Calculate screen dimensions
    screen_width = (GRID_COLS * BLOCK_SIZE) * 2 + BOARD_SPACING
    screen_height = GRID_ROWS * BLOCK_SIZE

    # Show start screen
    start_screen = StartScreen(screen_width, screen_height)
    selected_difficulty = start_screen.run()

    if selected_difficulty is None:
        return  # User closed window

    # Start game with selected difficulty
    game = Game(difficulty=selected_difficulty)
    game.run()


if __name__ == "__main__":
    main()
