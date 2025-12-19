import pygame
from battleship_game.board import Board
from battleship_game.config import GRID_COLS, GRID_ROWS, BLOCK_SIZE

def main():
    pygame.init()

    screen_width = (GRID_COLS * BLOCK_SIZE) * 2 + BLOCK_SIZE * 2
    screen_height = GRID_ROWS * BLOCK_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Battleship")

    # make two Boards
    left_board = Board(GRID_COLS, GRID_ROWS, BLOCK_SIZE)
    right_board = Board(GRID_COLS, GRID_ROWS, BLOCK_SIZE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # Left Board (Gamer)
        left_board.draw(screen, offset_x=0)

        # Right Board (Computer) -> move to the right
        offset_right = GRID_COLS * BLOCK_SIZE + BLOCK_SIZE * 2
        right_board.draw(screen, offset_x=offset_right)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()


