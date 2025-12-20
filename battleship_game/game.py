import pygame
from battleship_game.board import Board
from battleship_game.fleet_commander import FleetManager
from battleship_game.config import GRID_COLS, GRID_ROWS, BLOCK_SIZE


class Game:
    def __init__(self):
        pygame.init()

        # Windowsize
        self.screen_width = (GRID_COLS * BLOCK_SIZE) * 2 + BLOCK_SIZE * 2
        self.screen_height = GRID_ROWS * BLOCK_SIZE
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        pygame.display.set_caption("Battleship")

        # Boards
        self.player_board = Board()
        self.enemy_board = Board()

        # fleet of the gamer
        self.fleet_manager = FleetManager(self.player_board)

        # the ship that is placed at the moment
        self.current_ship_index = 0
        self.current_orientation = "hor"

        # Offset for the right Board
        self.enemy_offset_x = GRID_COLS * BLOCK_SIZE + BLOCK_SIZE * 2

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # change ship direction
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.current_orientation = "ver" if self.current_orientation == "hor" else "hor"

                # mouse clic for placement
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)

            self.draw()
            pygame.display.flip()

        pygame.quit()

    def handle_mouse_click(self, pos):
        """place the ship on the left board."""
        x_pixel, y_pixel = pos

        # mouse clic has to be in the left board.
        if x_pixel > GRID_COLS * BLOCK_SIZE:
            return

        # convert in Grid-coordinates
        x = x_pixel // BLOCK_SIZE
        y = y_pixel // BLOCK_SIZE

        ship = self.fleet_manager.ships[self.current_ship_index]

        if self.fleet_manager.place_ship(ship, x, y, self.current_orientation):
            print(f"Placed ship {self.current_ship_index} at {x},{y}")

            self.current_ship_index += 1

            if self.current_ship_index >= len(self.fleet_manager.ships):
                print("All ships placed!")
                # later on: Start game

    def draw(self):
        self.screen.fill((0, 0, 0))

        # show Boards
        self.player_board.draw(self.screen, offset_x=0)
        self.enemy_board.draw(self.screen, offset_x=self.enemy_offset_x)
