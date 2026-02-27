"""Start screen for Battleship game with difficulty selection using factory pattern."""

import pygame
from battleship_game.config import (
    COLOR_TEXT,
    COLOR_SHIP,
    COLOR_GRID,
    COLOR_OVERLAY,
    OVERLAY_ALPHA,
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_BUTTON,
    FONT_GAMEOVER,
    BUTTON_WIDTH_FACTOR,
    BUTTON_HEIGHT_FACTOR,
    BUTTON_REPLAY_Y,
    BUTTON_MENU_Y,
    main_bg,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)


class StartScreen:
    """
    Start screen for Battleship game with difficulty selection.
    """

    def __init__(self, screen: pygame.Surface, game_factories: list[type]):
        """
        Initialize the start screen.

        Args:
            screen: Pygame display surface
            game_factories: List of GameFactory classes to choose from
        """
        self.screen = screen
        self.game_factories = game_factories

        # Background
        self.bg_img = pygame.image.load(main_bg).convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.SysFont(None, FONT_TITLE)
        self.button_font = pygame.font.SysFont(None, FONT_SUBTITLE)
        self.subtitle_font = pygame.font.SysFont(None, FONT_BUTTON)

        # Selected factory (None until a button is clicked)
        self.selected_factory = None

    def _create_buttons(self):
        """
        Create button rectangles for each difficulty level.

        Returns:
            List of tuples (factory_class, pygame.Rect)
        """
        buttons = []
        w = self.screen.get_width()
        h = self.screen.get_height()

        button_width = 200
        button_height = 60
        spacing = 20

        total_height = len(self.game_factories) * (button_height + spacing) - spacing
        start_y = (h - total_height) // 2 + 80

        for i, factory in enumerate(self.game_factories):
            rect = pygame.Rect(
                (w - button_width) // 2,
                start_y + i * (button_height + spacing),
                button_width,
                button_height,
            )
            buttons.append((factory, rect))
        return buttons

    def draw(self):
        """
        Render the start screen including title, subtitle, and difficulty buttons.

        Args:
            None. Uses internal screen states and mouse position.

        Returns:
            None. Draws directly onto the display surface.
        """
        w = self.screen.get_width()

        title = self.title_font.render("BATTLESHIP", True, COLOR_TEXT)
        self.screen.blit(title, title.get_rect(center=(w // 2, 80)))

        subtitle = self.subtitle_font.render("Select Difficulty", True, COLOR_SHIP)
        self.screen.blit(subtitle, subtitle.get_rect(center=(w // 2, 140)))

        buttons = self._create_buttons()
        mouse = pygame.mouse.get_pos()

        for factory, rect in buttons:
            hovered = rect.collidepoint(mouse)
            color = COLOR_SHIP if hovered else COLOR_GRID

            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, COLOR_TEXT, rect, 2)

            label = factory.__name__.replace("Battleship", "")
            text = self.button_font.render(label, True, COLOR_TEXT)
            self.screen.blit(text, text.get_rect(center=rect.center))

        pygame.display.flip()

    def run(self, events):
        """
        Update the start screen and return the selected difficulty factory if clicked.

        Args:
            events: List of Pygame events for the current frame.

        Returns:
            The selected GameFactory class if a button was clicked, otherwise None.
        """
        self.screen.blit(self.bg_img, (0, 0))
        self.draw()
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                for factory, rect in self._create_buttons():
                    if rect.collidepoint(e.pos):
                        return factory
        return None


class GameOverScreen:
    """Screen shown after the game ends, offering replay or return to menu."""

    def __init__(self, screen):
        """
        Initialize the game‑over screen with fonts and display surface.

        Args:
            screen: Pygame display surface.
        """
        self.screen = screen
        self.font = pygame.font.SysFont(None, FONT_GAMEOVER)
        self.button_font = pygame.font.SysFont(None, FONT_BUTTON)

    def run(self, state, events):
        """
        Render the game‑over overlay and handle replay/menu button clicks.

        Args:
            state: Current game‑over states (win or loss).
            events: List of Pygame events for the current frame.

        Returns:
            2 if replay was selected,
            1 if return to menu was selected,
            otherwise the unchanged states.
        """
        w, h = self.screen.get_size()

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((*COLOR_OVERLAY, OVERLAY_ALPHA))
        self.screen.blit(overlay, (0, 0))

        button_w = int(w * BUTTON_WIDTH_FACTOR)
        button_h = int(h * BUTTON_HEIGHT_FACTOR)

        replay_rect = pygame.Rect(
            (w - button_w) // 2,
            int(h * BUTTON_REPLAY_Y),
            button_w,
            button_h,
        )

        menu_rect = pygame.Rect(
            (w - button_w) // 2,
            int(h * BUTTON_MENU_Y),
            button_w,
            button_h,
        )

        mouse = pygame.mouse.get_pos()

        self._draw_button("Replay", replay_rect, mouse)
        self._draw_button("Main Menu", menu_rect, mouse)

        pygame.display.flip()

        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if replay_rect.collidepoint(e.pos):
                    return 2
                if menu_rect.collidepoint(e.pos):
                    return 1

        return state

    def _draw_button(self, text, rect, mouse):
        """
        Draw a single interactive button with hover highlighting.

        Args:
            text: Button label.
            rect: Button rectangle.
            mouse: Current mouse position.

        Returns:
            None. Draws directly onto the display surface.
        """
        hovered = rect.collidepoint(mouse)
        color = COLOR_GRID if hovered else COLOR_SHIP

        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, COLOR_TEXT, rect, 2)

        label = self.button_font.render(text, True, COLOR_TEXT)
        self.screen.blit(label, label.get_rect(center=rect.center))
