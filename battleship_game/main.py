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

def draw_ship_cell(surface, x: int, y: int):
    pos_x = BLOCK_SIZE * x
    pos_y = BLOCK_SIZE * y

    # draw cell
    pygame.draw.rect(surface, GRAY, (pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE))

    # draw border around the cell
    pygame.draw.rect(surface, COLOR_GRID, (pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE), width=2)

def draw_ship(size: int, orientation: str, surface, x: int, y: int) -> None:
    if orientation == "hor":
        for l in range(1, size + 1):
            draw_ship_cell(surface, x + l, y)
    else:
        for l in range(1, size + 1):
            draw_ship_cell(surface, x, y + l)

    ...

if __name__ == "__main__":
    main()

