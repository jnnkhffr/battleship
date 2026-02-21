"""Start screen for Battleship game with difficulty selection using factory pattern."""

import pygame
from battleship_game.config import (
    COLOR_BG,
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
)


class StartScreen:
    """
    Start screen for Battleship game with difficulty selection.

    Works with GameFactory classes to select and create games.
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
        self.screen.fill(COLOR_BG)
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
        self.draw()
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                for factory, rect in self._create_buttons():
                    if rect.collidepoint(e.pos):
                        return factory
        return None

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, FONT_GAMEOVER)
        self.button_font = pygame.font.SysFont(None, FONT_BUTTON)

    def run(self, state, events):
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
        hovered = rect.collidepoint(mouse)
        color = COLOR_GRID if hovered else COLOR_SHIP

        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, COLOR_TEXT, rect, 2)

        label = self.button_font.render(text, True, COLOR_TEXT)
        self.screen.blit(label, label.get_rect(center=rect.center))
