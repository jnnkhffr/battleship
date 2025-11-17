import pygame
from battleship_game.board import Board
from battleship_game.config import GRID_COLS, GRID_ROWS, BLOCK_SIZE

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((GRID_COLS * BLOCK_SIZE, GRID_ROWS * BLOCK_SIZE))
    pygame.display.set_caption("Battleship")

    board = Board(GRID_COLS, GRID_ROWS, BLOCK_SIZE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        board.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

