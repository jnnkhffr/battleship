"""Main module to run the Battleship game."""

import pygame
from enum import Enum

from battleship_game.game import BattleshipEasy, BattleshipMedium, BattleshipHard
from battleship_game.start_screen import StartScreen
from battleship_game.config import GRID_COLS, GRID_ROWS, BLOCK_SIZE, BOARD_SPACING


class GameState(Enum):
    """Game state enum."""

    SELECTING = 1
    NEW = 2
    RUNNING = 3
    WIN = 4
    LOSS = 5


class GameHandler:
    """Main game handler that manages game states and transitions."""

    def __init__(self, game_factories: list[type]):
        """
        Initialize the game handler.

        Args:
            game_factories: List of GameFactory classes to offer as choices
        """
        pygame.init()
        pygame.font.init()

        # Calculate window size
        self.screen_width = (GRID_COLS * BLOCK_SIZE) * 2 + BOARD_SPACING
        self.screen_height = GRID_ROWS * BLOCK_SIZE

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Battleship")

        self.clock = pygame.time.Clock()
        self.running = True

        self.game_factories = game_factories
        self._selected_game_factory = None

        # Create start screen
        self.start_screen = StartScreen(self.screen, game_factories)

    def run(self):
        """Run the main game loop."""
        current_game = None
        game_state = GameState.SELECTING

        while self.running:
            events = pygame.event.get()

            # Check for quit event
            if any(event.type == pygame.QUIT for event in events):
                self.running = False
                continue

            if game_state == GameState.SELECTING:
                # Show start screen and wait for selection
                selected_factory_class = self.start_screen.run(events)
                if selected_factory_class is not None:
                    # Create factory instance with screen and clock
                    self._selected_game_factory = selected_factory_class(
                        self.screen, self.clock
                    )
                    game_state = GameState.NEW

            elif game_state == GameState.NEW:
                # Create new game from selected factory
                current_game = self._selected_game_factory.create()
                game_state = GameState.RUNNING

            elif game_state == GameState.RUNNING:
                # Run the game and check if it's still running
                still_running = current_game.run(events)

                if not still_running:
                    # Game ended - check if won or lost
                    if current_game.game_over_message == "You win!":
                        game_state = GameState.WIN
                    else:
                        game_state = GameState.LOSS

            elif game_state in (GameState.WIN, GameState.LOSS):
                # Show game over screen and handle replay/menu options
                game_state = self.game_over_screen(game_state, events)

            self.clock.tick(60)

        pygame.quit()

    def game_over_screen(
        self, game_state: GameState, events: list[pygame.event.Event]
    ) -> GameState:
        """
        Render the game over screen with replay and menu options.

        Args:
            game_state: Current game state (WIN or LOSS)
            events: List of pygame events

        Returns:
            Next game state
        """
        # Draw semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Draw win/loss message
        msg = "You Win!" if game_state == GameState.WIN else "You Lost!"
        big_font = pygame.font.Font(pygame.font.get_default_font(), 48)
        text_surf = big_font.render(msg, True, (255, 255, 255))
        text_rect = text_surf.get_rect(
            center=(self.screen_width // 2, self.screen_height // 4)
        )
        self.screen.blit(text_surf, text_rect)

        # Create buttons
        button_width = int(self.screen_width * 0.35)
        button_height = int(self.screen_height * 0.08)
        center_x = self.screen_width // 2

        replay_button = pygame.Rect(
            center_x - button_width // 2,
            int(self.screen_height * 0.55),
            button_width,
            button_height,
        )

        menu_button = pygame.Rect(
            center_x - button_width // 2,
            int(self.screen_height * 0.68),
            button_width,
            button_height,
        )

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        small_font = pygame.font.Font(pygame.font.get_default_font(), 30)

        self._draw_button(
            "Replay",
            replay_button,
            small_font,
            (255, 255, 255),
            (70, 130, 180),
            (100, 160, 210),
            mouse_pos,
        )

        self._draw_button(
            "Main Menu",
            menu_button,
            small_font,
            (255, 255, 255),
            (180, 70, 70),
            (210, 100, 100),
            mouse_pos,
        )

        # Handle button clicks
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(event.pos):
                    return GameState.NEW

                if menu_button.collidepoint(event.pos):
                    return GameState.SELECTING

        pygame.display.flip()
        return game_state

    def _draw_button(
        self, text, rect, font, text_color, button_color, hover_color, mouse_pos
    ):
        """Draw a button with hover effect."""
        color = hover_color if rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)


def main():
    """Main entry point for the Battleship game."""
    game_handler = GameHandler([BattleshipEasy, BattleshipMedium, BattleshipHard])
    game_handler.run()


if __name__ == "__main__":
    main()
