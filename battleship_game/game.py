"""Game module with factory pattern for different difficulty levels."""

from __future__ import annotations
from abc import ABC, abstractmethod

import pygame
import random
from battleship_game.board import Board
from battleship_game.fleet_commander import FleetManager
from battleship_game.config import (
    GRID_COLS,
    GRID_ROWS,
    BLOCK_SIZE,
    BOARD_SPACING,
    DEFAULT_ORIENTATION,
    COLOR_BG,
    COLOR_GRID,
    COLOR_MESSAGE,
    COLOR_MESSAGE_FIRING,
    DEBUG_SHOW_ENEMY_SHIPS,
    DURATION,
    DELAY,
)
from battleship_game.computer_fleet import ComputerFleetManager

from battleship_game.ai_shooting import (
    RandomShootingStrategy,
    HuntShootingStrategy,
    SmartShootingStrategy,
)


class Game:
    """
    Main game controller class.

    Responsibilities:
    - Initialize window and rendering
    - Manage player and enemy boards
    - Handle ship placement phase
    - Transition into shooting phase once placement is complete
    """

    def __init__(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        difficulty_name: str = "",
    ):
        """
        Initialize the game environment, create boards, fleet manager,
        and prepare the placement phase.

        Args:
            screen: Pygame display surface
            clock: Pygame clock for timing
            difficulty_name: Name of the difficulty (for window caption)
        """
        self.screen = screen
        self.clock = clock

        # Calculate window size
        self.screen_width = (GRID_COLS * BLOCK_SIZE) * 2 + BOARD_SPACING
        self.screen_height = GRID_ROWS * BLOCK_SIZE

        # Set caption
        caption = (
            "Battleship" if not difficulty_name else f"Battleship - {difficulty_name}"
        )
        pygame.display.set_caption(caption)

        # Boards
        self.player_board = Board()
        self.enemy_board = Board()

        # Player fleet
        self.fleet_manager = FleetManager(self.player_board)

        # Index of the ship currently being placed
        self.current_ship_index = 0

        # Default orientation for placement
        self.current_orientation = DEFAULT_ORIENTATION

        # Offset for drawing the enemy board
        self.enemy_offset_x = GRID_COLS * BLOCK_SIZE + BOARD_SPACING

        # True once all ships have been placed
        self.placement_done = False

        # Game over
        self.game_over = False
        self.game_over_message = ""

        # preview tracking
        self.mouse_grid_pos = (0, 0)
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 64)
        # self.top_margin = 0
        self.battle_message_start = None
        self.battle_message_duration = DURATION
        self.battle_message_surface = self.font.render("THE BATTLE STARTS!", True, COLOR_MESSAGE_FIRING)

        self.player_turn = True
        self.enemy_turn_pending = False
        self.enemy_turn_time = 0
        self.enemy_delay = DELAY


    def run(self, events: list[pygame.event.Event]) -> bool:
        """
        Main game loop iteration.
        Handles events, updates the game state, and renders the Boards.

        Args:
            events: List of pygame events to process

        Returns:
            True if game is still running, False if game over
        """
        for event in events:
            # Rotate ship during placement phase
            if not self.placement_done and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.current_orientation = (
                        "ver" if self.current_orientation == "hor" else "hor"
                    )

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

            if event.type == pygame.MOUSEMOTION:
                self.mouse_grid_pos = event.pos

            # Delay of computer shooting
            if self.enemy_turn_pending:
                now = pygame.time.get_ticks()
                if now - self.enemy_turn_time >= self.enemy_delay:
                    self.enemy_turn()
                    self.enemy_turn_pending = False
                    self.player_turn = True

        self.draw()
        pygame.display.flip()
        self.clock.tick(60)

        return not self.game_over

    def handle_mouse_click(self, pos):
        """
        Handle mouse clicks depending on the current game phase.

        Placement phase:
            - Convert mouse position to grid coordinates
            - Attempt to place the next ship on the player's board

        Shooting phase:
            - (Future) Handle firing shots at the enemy board
        """
        if not self.player_turn:
            return

        if self.game_over:
            return

        x_pixel, y_pixel = pos

        # SHOOTING PHASE
        if self.placement_done:
            # Ignore clicks on player board
            if x_pixel < self.enemy_offset_x:
                return

            # Convert to grid
            x = (x_pixel - self.enemy_offset_x) // BLOCK_SIZE
            y = y_pixel // BLOCK_SIZE

            # Validate grid bounds
            if not (0 <= x < GRID_COLS and 0 <= y < GRID_ROWS):
                return

            # Prevent double shots
            if self.enemy_board.grid[y][x] in [2, 3, 4]:
                print("You already shot here")
                return

            # Player shoots
            ship_hit = self.enemy_fleet.receive_shot(x, y)

            if ship_hit:
                self.enemy_board.hit(x, y)
                print("Hit!")

                if ship_hit.is_sunk():
                    self.enemy_board.sunk(ship_hit)
                    print(f"You sunk the enemy {ship_hit.name}")

                    if self.enemy_fleet.is_defeated():
                        print("You win!")
                        self.game_over = True
                        self.game_over_message = "You win!"
                        self.placement_done = True
                        return
            else:
                self.enemy_board.miss(x, y)
                print("Miss")

            # Enemy turn
            self.player_turn = False
            self.enemy_turn_pending = True
            self.enemy_turn_time = pygame.time.get_ticks()
            return

        # PLACEMENT PHASE
        if x_pixel > GRID_COLS * BLOCK_SIZE:
            return

        x = x_pixel // BLOCK_SIZE
        y = y_pixel // BLOCK_SIZE

        if self.current_ship_index >= len(self.fleet_manager.ships):
            self.placement_done = True
            self.battle_message_start = pygame.time.get_ticks()
            print("All ships placed. Shooting mode enabled.")
            return

        ship = self.fleet_manager.ships[self.current_ship_index]

        if self.fleet_manager.place_ship(ship, x, y, self.current_orientation):
            print(f"Placed {ship.name} at {x},{y}")
            self.current_ship_index += 1

            if self.current_ship_index >= len(self.fleet_manager.ships):
                self.placement_done = True
                self.battle_message_start = pygame.time.get_ticks()
                print("All ships placed! Shooting mode active.")

    def draw(self):
        """Render both screens on the board."""
        self.screen.fill(COLOR_BG)

        preview = None
        if (
            not self.placement_done
            and self.current_ship_index < len(self.fleet_manager.ships)
            and not self.game_over
        ):
            mx, my = getattr(self, "mouse_grid_pos", (0, 0))
            if mx < GRID_COLS * BLOCK_SIZE:
                gx = mx // BLOCK_SIZE
                gy = my // BLOCK_SIZE
                ship = self.fleet_manager.ships[self.current_ship_index]
                valid = self.player_board.can_place_ship(
                    gx, gy, ship.size, self.current_orientation
                )
                preview = {
                    "x": gx,
                    "y": gy,
                    "size": ship.size,
                    "orientation": self.current_orientation,
                    "alpha": 128,  # 50% Transparency
                    "valid": valid,
                }

        # Draw player's board with preview
        self.player_board.draw(self.screen, offset_x=0, offset_y=0, preview=preview)

        # Draw enemy's board once
        self.enemy_board.draw(self.screen, offset_x=self.enemy_offset_x, offset_y=0)

        # If DEBUG off: overpaint enemy ships
        if not DEBUG_SHOW_ENEMY_SHIPS:
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

        # Show battle start message for 3 seconds
        if self.battle_message_start is not None and not self.game_over:
            elapsed = pygame.time.get_ticks() - self.battle_message_start
            if elapsed < self.battle_message_duration:
                text_rect = self.battle_message_surface.get_rect(
                    center=(self.screen_width // 2, self.screen_height // 2)
                )
                self.screen.blit(self.battle_message_surface, text_rect)
            else:
                # Stops after 3 Seconds
                self.battle_message_start = None

        # Game over message
        if self.game_over and self.game_over_message:
            text_surface = self.font.render(self.game_over_message, True, COLOR_MESSAGE)
            text_rect = text_surface.get_rect(
                center=(self.screen_width // 2, self.screen_height // 4)
            )
            self.screen.blit(text_surface, text_rect)

    def enemy_turn(self):
        if self.game_over:
            return
        # Co-ordinates of shooting
        x, y = self.enemy_fleet.get_next_shot(self.player_board)
        ship_hit = self.fleet_manager.receive_shot(x, y)

        if ship_hit:
            self.player_board.hit(x, y)
            print("Enemy hit!")
            sunk = ship_hit.is_sunk()

            if sunk:
                self.player_board.sunk(ship_hit)
                print(f"Enemy sunk your {ship_hit.name}")

            self.enemy_fleet.strategy.register_shot_result(
                x, y,
                hit=True,
                sunk=sunk
            )

            if self.fleet_manager.is_defeated():
                print("Computer wins!")
                self.game_over = True
                self.game_over_message = "You lost!"
                return
        else:
            self.player_board.miss(x, y)
            print("Enemy miss")

            self.enemy_fleet.strategy.register_shot_result(
                x, y,
                hit=False,
                sunk=False
            )


class GameFactory(ABC):
    """Abstract factory class to create Battleship games with different difficulties."""

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        """
        Initialize the factory.

        Args:
            screen: Pygame display surface
            clock: Pygame clock for timing
        """
        self._screen = screen
        self._clock = clock

    @abstractmethod
    def create(self) -> Game:
        """Create and return a Game instance."""
        ...


class BattleshipEasy(GameFactory):
    def create(self) -> Game:
        game = Game(self._screen, self._clock, "Easy")
        game.enemy_fleet = ComputerFleetManager(
            game.enemy_board, RandomShootingStrategy()
        )
        game.enemy_fleet.auto_place_fleet()
        return game


class BattleshipMedium(GameFactory):
    def create(self) -> Game:
        game = Game(self._screen, self._clock, "Medium")
        game.enemy_fleet = ComputerFleetManager(
            game.enemy_board, HuntShootingStrategy()
        )
        game.enemy_fleet.auto_place_fleet()
        return game


class BattleshipHard(GameFactory):
    def create(self) -> Game:
        game = Game(self._screen, self._clock, "Hard")
        game.enemy_fleet = ComputerFleetManager(
            game.enemy_board, SmartShootingStrategy()
        )
        game.enemy_fleet.auto_place_fleet()
        return game
