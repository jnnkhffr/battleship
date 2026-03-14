"""Game module with factory pattern for different difficulty levels."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod

import pygame

from battleship_game.board import Board
from battleship_game.fleet_commander import FleetManager
from battleship_game.config import (
    GRID_COLS,
    GRID_ROWS,
    BLOCK_SIZE,
    BOARD_SPACING,
    DEFAULT_ORIENTATION,
    COLOR_BG,
    COLOR_MESSAGE,
    COLOR_MESSAGE_FIRING,
    DEBUG_SHOW_ENEMY_SHIPS,
    DURATION,
    DELAY,
    HIT_SOUND,
    MISS_SOUND,
    SUNK_SOUND,
    HIT_TOKEN,
    MISS_TOKEN,
    SUNK_TOKEN,
    PLAYER_GRID,
    ENEMY_GRID,
    SHIP_DATA,
    ALPHA_PREVIEW,
    HIT_SOUND_VOL,
    MISS_SOUND_VOL,
    SUNK_SOUND_VOL,
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

        self.screen_width = (GRID_COLS * BLOCK_SIZE) * 2 + BOARD_SPACING
        self.screen_height = GRID_ROWS * BLOCK_SIZE

        caption = (
            "Battleship" if not difficulty_name else f"Battleship - {difficulty_name}"
        )
        pygame.display.set_caption(caption)

        # Boards
        self.player_board = Board(grid_image_path=PLAYER_GRID)
        self.enemy_board = Board(grid_image_path=ENEMY_GRID)

        # Player fleet
        self.fleet_manager = FleetManager(self.player_board)

        # Enemy fleet
        self.enemy_fleet: ComputerFleetManager | None = None

        # Index of the ship currently being placed
        self.current_ship_index = 0

        self.current_orientation = DEFAULT_ORIENTATION

        self.enemy_offset_x = GRID_COLS * BLOCK_SIZE + BOARD_SPACING

        # True once all ships have been placed
        self.placement_done = False

        self.game_over = False
        self.game_over_message = ""

        # preview tracking
        self.mouse_grid_pos = (0, 0)
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 64)
        self.battle_message_start = None
        self.battle_message_duration = DURATION
        self.battle_message_surface = self.font.render(
            "THE BATTLE STARTS!", True, COLOR_MESSAGE_FIRING
        )

        self.player_turn = True
        self.enemy_turn_pending = False
        self.enemy_turn_time = 0
        self.enemy_delay = DELAY

        # container for holding images
        self.ship_images = {}

        # Load ships directly from config
        for name, (size, path) in SHIP_DATA.items():
            img = pygame.image.load(path).convert_alpha()

            # Scale the images to fit the grid
            scaled_img = pygame.transform.scale(img, (BLOCK_SIZE, BLOCK_SIZE * size))
            self.ship_images[name] = scaled_img

        # Loading animations using frames
        self.fire_animation = []
        for i in range(1, 14):
            frame_path = f"assets/images/tokens/fireloop/fire1_{i:02}.png"
            img_fire = pygame.image.load(frame_path)
            self.fire_animation.append(img_fire)

        self.hit_sound = pygame.mixer.Sound(HIT_SOUND)
        self.miss_sound = pygame.mixer.Sound(MISS_SOUND)
        self.sunk_sound = pygame.mixer.Sound(SUNK_SOUND)
        self.hit_sound.set_volume(HIT_SOUND_VOL)
        self.miss_sound.set_volume(MISS_SOUND_VOL)
        self.sunk_sound.set_volume(SUNK_SOUND_VOL)

        self.miss_token = pygame.image.load(MISS_TOKEN)
        self.hit_token = pygame.image.load(HIT_TOKEN)
        self.sunk_token = pygame.image.load(SUNK_TOKEN)

        self.miss_token = pygame.transform.scale(
            self.miss_token, (BLOCK_SIZE, BLOCK_SIZE)
        )
        self.hit_token = pygame.transform.scale(
            self.hit_token, (BLOCK_SIZE, BLOCK_SIZE)
        )
        self.sunk_token = pygame.transform.scale(
            self.sunk_token, (BLOCK_SIZE, BLOCK_SIZE)
        )

        self.tokens = {2: self.miss_token, 3: self.hit_token, 4: self.sunk_token}

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
        Handle mouse click actions depending on the current game phase.

        During placement:
            Converts the mouse position into grid coordinates and attempts
            to place the next ship on the player's board.

        During shooting:
            Converts the mouse position into enemy grid coordinates,
            validates the shot, applies hit/miss logic, and checks for win conditions.

        Args:
            pos: Mouse click position as (x, y) pixel coordinates.

        Returns:
            None. The method updates game state, triggers ship placement,
            processes shots, and may set the game-over state.
        """

        if not self.player_turn:
            return

        if self.game_over:
            return

        x_pixel, y_pixel = pos

        # SHOOTING PHASE
        if self.placement_done:
            if x_pixel < self.enemy_offset_x:
                return

            # Convert to grid
            x = (x_pixel - self.enemy_offset_x) // BLOCK_SIZE
            y = y_pixel // BLOCK_SIZE

            # Validate grid bounds
            if not (0 <= x < GRID_COLS and 0 <= y < GRID_ROWS):
                return

            if self.enemy_board.grid[y][x] in [2, 3, 4]:
                # TODO: replace prints with logging
                # print("You already shot here")
                logging.debug("You already shot here")
                return

            # TODO: you need to set the enemy_fleet in the init. The game runs because
            #  it is explicitly set in each factory. A user might not know he needs to
            #  do this and will break the code. Make the ComputerFleetManager part of
            #  the init.
            #  Since there are some circular usage of enemy board, consider making the
            #  ShootingStrategy an arg.
            ship_hit = self.enemy_fleet.receive_shot(x, y)

            if ship_hit:
                self.enemy_board.hit(x, y)
                self.hit_sound.play()
                # TODO: replace prints with logging
                print("Hit!")

                if ship_hit.is_sunk():
                    self.enemy_board.sunk(ship_hit)
                    self.sunk_sound.play()
                    # TODO: replace prints with logging
                    print(f"You sunk the enemy {ship_hit.name}")

                    # TODO: unnecessary level of indentation? in enemy turn it does not
                    if self.enemy_fleet.is_defeated():
                        # TODO: replace prints with logging
                        print("You win!")
                        self.game_over = True
                        self.game_over_message = "You win!"
                        self.placement_done = True
                        return
            else:
                self.enemy_board.miss(x, y)
                self.miss_sound.play()
                # TODO: replace prints with logging
                print("Miss")

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
            # TODO: replace prints with logging
            print("All ships placed. Shooting mode enabled.")
            return

        ship = self.fleet_manager.ships[self.current_ship_index]

        if self.fleet_manager.place_ship(ship, x, y, self.current_orientation):
            # TODO: replace prints with logging
            print(f"Placed {ship.name} at {x},{y}")
            self.current_ship_index += 1

            if self.current_ship_index >= len(self.fleet_manager.ships):
                self.placement_done = True
                self.battle_message_start = pygame.time.get_ticks()
                # TODO: replace prints with logging
                print("All ships placed! Shooting mode active.")

    def draw(self):
        """
        Render the full game screen including both boards, placement previews,
        battle messages, and game‑over messages.

        Args:
            None. Uses internal game state such as placement progress,
            mouse position, fleet status, and timing values.

        Returns:
            None. The method updates the visual output on the main screen
            by drawing player and enemy boards, ship previews, and messages.
        """
        self.screen.fill(COLOR_BG)

        preview = None
        if (
            not self.placement_done
            and self.current_ship_index < len(self.fleet_manager.ships)
            and not self.game_over
        ):
            # TODO: why do you use getattr?
            mx, my = self.mouse_grid_pos
            # mx, my = getattr(self, "mouse_grid_pos", (0, 0))
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
                    "ship": ship,
                    "orientation": self.current_orientation,
                    "alpha": ALPHA_PREVIEW,  # 50% Transparency
                    "valid": valid,
                }

        # Draw player's board with preview
        self.player_board.draw(
            self.screen,
            offset_x=0,
            offset_y=0,
            preview=preview,
            token_images=self.tokens,
            ship_images=self.ship_images,
            fleet=self.fleet_manager,
        )

        # Draw enemy's board once
        self.enemy_board.draw(
            self.screen,
            offset_x=self.enemy_offset_x,
            offset_y=0,
            token_images=self.tokens,
            ship_images=self.ship_images,
            fleet=self.enemy_fleet,
            show_ships=DEBUG_SHOW_ENEMY_SHIPS,
        )

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
        """
        Execute the enemy's turn by selecting a target, applying hit or miss logic,
        updating board state, and checking for defeat conditions.

        Args:
            None. Uses the enemy fleet's targeting strategy and the player's board state.

        Returns:
            None. Updates the player's board, registers shot results in the enemy AI,
            and may set the game-over state if all player ships are destroyed.
        """
        if self.game_over:
            return

        x, y = self.enemy_fleet.get_next_shot(self.player_board)
        ship_hit = self.fleet_manager.receive_shot(x, y)

        if ship_hit:
            self.player_board.hit(x, y)
            self.hit_sound.play()
            # TODO: replace prints with logging
            print("Enemy hit!")
            sunk = ship_hit.is_sunk()

            if sunk:
                self.player_board.sunk(ship_hit)
                self.sunk_sound.play()
                # TODO: replace prints with logging
                print(f"Enemy sunk your {ship_hit.name}")

            self.enemy_fleet.strategy.register_shot_result(x, y, hit=True, sunk=sunk)

            if self.fleet_manager.is_defeated():
                # TODO: replace prints with logging
                print("Computer wins!")
                self.game_over = True
                self.game_over_message = "You lost!"
                return
        else:
            self.player_board.miss(x, y)
            self.miss_sound.play()
            # TODO: replace prints with logging
            print("Enemy miss")

            self.enemy_fleet.strategy.register_shot_result(x, y, hit=False, sunk=False)


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


# TODO: check line length (88 chars)
class BattleshipEasy(GameFactory):
    """Factory for creating a Battleship game configured with easy difficulty and random enemy shooting."""

    def create(self) -> Game:
        """
        Create a new Game instance configured for the Easy difficulty.

        Args:
            None. Uses the factory's screen and clock to initialize the game.

        Returns:
            A fully initialized Game object with an enemy fleet that uses
            random shooting behavior and automatically placed ships.
        """
        game = Game(self._screen, self._clock, "Easy")
        game.enemy_fleet = ComputerFleetManager(
            game.enemy_board, RandomShootingStrategy()
        )
        game.enemy_fleet.auto_place_fleet()
        return game


class BattleshipMedium(GameFactory):
    """
    Factory for creating a Battleship game with medium difficulty
    using a hunt-based enemy strategy.
    """

    def create(self) -> Game:
        """
        Create a new Game instance configured for the Medium difficulty.

        Args:
            None. Uses the factory's screen and clock to initialize the game.

        Returns:
            A fully initialized Game object with an enemy fleet that uses
            a hunt-based shooting strategy and automatically placed ships.
        """
        game = Game(self._screen, self._clock, "Medium")
        game.enemy_fleet = ComputerFleetManager(
            game.enemy_board, HuntShootingStrategy()
        )
        game.enemy_fleet.auto_place_fleet()
        return game


class BattleshipHard(GameFactory):
    """Factory for creating a Battleship game with hard difficulty using an advanced enemy strategy."""

    def create(self) -> Game:
        """
        Create a new Game instance configured for the Hard difficulty.

        Args:
            None. Uses the factory's screen and clock to initialize the game.

        Returns:
            A fully initialized Game object with an enemy fleet that uses
            an advanced smart shooting strategy and automatically placed ships.
        """
        game = Game(self._screen, self._clock, "Hard")
        game.enemy_fleet = ComputerFleetManager(
            game.enemy_board, SmartShootingStrategy()
        )
        game.enemy_fleet.auto_place_fleet()
        return game
