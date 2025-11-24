import pygame
from battleship_game.board import Board
from battleship_game.config import GRID_COLS, GRID_ROWS, BLOCK_SIZE

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(((GRID_COLS + 1) * BLOCK_SIZE * 2 , GRID_ROWS * BLOCK_SIZE)) # create a screen which has the size of 22 grid cells
    pygame.display.set_caption("Battleship")

    board = Board(GRID_COLS, GRID_ROWS, BLOCK_SIZE)

    left_board = Board(GRID_COLS, GRID_ROWS, BLOCK_SIZE)
    right_board = Board(GRID_COLS, GRID_ROWS, BLOCK_SIZE)
    #middle_line =

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        left_board.draw(screen, offset_x=0)
        right_board.draw(screen, offset_x=(GRID_COLS + 2)  * BLOCK_SIZE) # move right board to the right edge with the + 2
        pygame.display.flip()

    pygame.quit()


#in construction

def place_ship_on_board(board, ship):
    ...

if __name__ == "__main__":
    main()

