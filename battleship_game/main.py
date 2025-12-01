import pygame
from battleship_game.board import Board
from battleship_game.config import GRID_COLS, GRID_ROWS, BLOCK_SIZE
from battleship_game.fleet import Fleet


# Initialize pygame
def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((GRID_COLS * BLOCK_SIZE, GRID_ROWS * BLOCK_SIZE))
    pygame.display.set_caption("Battleship")
    board = Board(GRID_COLS, GRID_ROWS, BLOCK_SIZE)
    player_fleet = Fleet()

    # Loop with registering mouse click
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Store mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # grid coordinates from the clicks
                col = mouse_x // BLOCK_SIZE
                row = mouse_y // BLOCK_SIZE
                # player fleet placement
                player_fleet.try_place_ship(row, col)

        screen.fill((0, 0, 0))  # clear screen
        board.draw(screen)  # draw board
        player_fleet.draw(screen)  # draw player fleet
        pygame.display.flip()  # update display


# Exit
pygame.quit()

if __name__ == "__main__":
    main()
