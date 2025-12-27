import sys
import pygame
from battleship_game.config import (
    GRID_COLS,
    GRID_ROWS,
    BLOCK_SIZE,
    BOARD_SPACING,
    DEFAULT_ORIENTATION,
    COLOR_BG,
    COLOR_GRID,
    DEBUG_SHOW_ENEMY_SHIPS,
)
from battleship_game.board import Board
from battleship_game.fleet import Fleet


class Battleship:
    """
    The main window, input and the Game Logic
    """

    def __init__(self):
        # Start pygame
        pygame.init()

        # Calculate the window size
        # Calculate window size
        self.screen_width = (GRID_COLS * BLOCK_SIZE) * 2 + BOARD_SPACING
        self.screen_height = GRID_ROWS * BLOCK_SIZE
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        pygame.display.set_caption("Battleship")

        # Boards
        self.player_board = Board()
        self.enemy_board = Board()

        # Player fleet
        self.fleet_manager = Fleet(self.player_board)

        # Index of the ship currently being placed
        self.current_ship_index = 0

        # Default orientation for placement
        self.current_orientation = DEFAULT_ORIENTATION

        # Offset for drawing the enemy board
        self.enemy_offset_x = GRID_COLS * BLOCK_SIZE + BOARD_SPACING

        # True once all ships have been placed
        self.placement_done = False

        # Enemy fleet
        self.enemy_fleet = Fleet(self.enemy_board)
        self.enemy_fleet.auto_place_fleet()

    def run(self):
        """
        Main game loop.
        Handles events, updates the game state, and renders the Boards.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Rotate ship during placement phase
                if not self.placement_done and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.current_orientation = (
                            "ver" if self.current_orientation == "hor" else "hor"
                        )
                        print("Orientation changed to ", self.current_orientation)

                # Handle mouse clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)

            self.draw()
            pygame.display.flip()

        pygame.quit()

    def handle_mouse_click(self, pos):
        """
        Handle mouse clicks depending on the current game phase.

        Placement phase:
            - Convert mouse position to grid coordinates
            - Attempt to place the next ship on the player's board

        Shooting phase:
            - (Future) Handle firing shots at the enemy board
        """
        x_pixel, y_pixel = pos

        # If placement is finished, switch to shooting mode
        if self.placement_done:
            if x_pixel < self.enemy_offset_x:
                return

            # Convert to grid
            x = (x_pixel - self.enemy_offset_x) // BLOCK_SIZE
            y = y_pixel // BLOCK_SIZE

            # Validate the shots fired
            if 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS:
                # Prevent shooting the same space twice
                if self.enemy_board.grid[y][x] in [2, 3, 4]:
                    print("You already shot here")
                    return
                # Player shoots
                ship_hit = self.enemy_fleet.shot(x, y)
                if ship_hit:
                    self.enemy_board.hit(x, y)
                    ship_hit.hits += 1
                    print("Hit")
                    if ship_hit.is_sunk():
                        self.enemy_board.sunk(ship_hit)
                        print(f"You sunk the enemy {ship_hit.name}")

                else:
                    self.enemy_board.miss(x, y)
                    print("Miss")
            return

        # Only allow placement on the left board (gamers sea)
        if x_pixel > GRID_COLS * BLOCK_SIZE:
            return

        # Convert pixel position to grid coordinates
        x = x_pixel // BLOCK_SIZE
        y = y_pixel // BLOCK_SIZE

        # Safety check: if all ships are placed, finalize placement
        if self.current_ship_index >= len(self.fleet_manager.ships):
            self.placement_done = True
            print("All ships placed. Shooting mode enabled.")
            return

        # Get the ship that is currently being placed
        ship = self.fleet_manager.ships[self.current_ship_index]

        # Attempt to place the ship
        if self.fleet_manager.place_ship(ship, x, y, self.current_orientation):
            print(f"Placed {ship.name} at {x},{y}")
            self.current_ship_index += 1

            # If this was the last ship, switch to shooting mode
            if self.current_ship_index >= len(self.fleet_manager.ships):
                self.placement_done = True
                print("All ships placed! Shooting mode active.")

    def draw(self):
        """
        Render both boards onto the screen.
        """
        self.screen.fill(COLOR_BG)

        # Draw player's board on the left
        self.player_board.draw(self.screen, offset_x=0)

        # Draw enemy's board on the right
        self.enemy_board.draw(self.screen, offset_x=self.enemy_offset_x)

        # Draw enemy board on right
        if DEBUG_SHOW_ENEMY_SHIPS:
            # Draw ships normally
            self.enemy_board.draw(self.screen, offset_x=self.enemy_offset_x)
        else:
            # Draw only the grid, without ships
            self.enemy_board.draw(self.screen, offset_x=self.enemy_offset_x)
            # Overpaint ships with background color
            for y in range(self.enemy_board.rows):
                for x in range(self.enemy_board.cols):
                    if self.enemy_board.grid[y][x] == 1:
                        rect = pygame.Rect(
                            self.enemy_offset_x + x * BLOCK_SIZE,
                            y * BLOCK_SIZE,
                            BLOCK_SIZE,
                            BLOCK_SIZE,
                        )
                        pygame.draw.rect(self.screen, COLOR_BG, rect)
                        pygame.draw.rect(self.screen, COLOR_GRID, rect, 1)


if __name__ == "__main__":
    game = Battleship()
    game.run()
