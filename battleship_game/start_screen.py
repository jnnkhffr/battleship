import pygame
from battleship_game.config import COLOR_BG, COLOR_TEXT, COLOR_SHIP, COLOR_GRID


class StartScreen:
    """
    Start screen for Battleship game with difficulty selection.

    Displays game title and difficulty buttons.
    Returns the selected difficulty when a button is clicked.
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialize the start screen.

        Args:
            screen_width: Width of the game window
            screen_height: Height of the game window
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Battleship - Select Difficulty")

        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.SysFont(None, 72)
        self.button_font = pygame.font.SysFont(None, 48)
        self.subtitle_font = pygame.font.SysFont(None, 32)

        # Available difficulties
        self.difficulties = ["Easy", "Medium", "Hard"]

        # Create buttons
        self.buttons = self._create_buttons()

        # Selected difficulty (None until a button is clicked)
        self.selected_difficulty = None

    def _create_buttons(self):
        """
        Create button rectangles for each difficulty level.

        Returns:
            List of tuples (difficulty_name, pygame.Rect)
        """
        buttons = []
        button_width = 200
        button_height = 60
        button_spacing = 20

        # Calculate starting Y position to center buttons vertically
        total_height = button_height * len(self.difficulties) + button_spacing * (
            len(self.difficulties) - 1
        )
        start_y = (self.screen_height - total_height) // 2 + 80

        for i, difficulty in enumerate(self.difficulties):
            x = (self.screen_width - button_width) // 2
            y = start_y + i * (button_height + button_spacing)
            button_rect = pygame.Rect(x, y, button_width, button_height)
            buttons.append((difficulty, button_rect))

        return buttons

    def draw(self):
        """Draw the start screen with title and buttons."""
        self.screen.fill(COLOR_BG)

        # Draw title
        title_text = self.title_font.render("BATTLESHIP", True, COLOR_TEXT)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 80))
        self.screen.blit(title_text, title_rect)

        # Draw subtitle
        subtitle_text = self.subtitle_font.render("Select Difficulty", True, COLOR_SHIP)
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, 140))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()

        for difficulty, button_rect in self.buttons:
            # Check if mouse is hovering over button
            is_hovered = button_rect.collidepoint(mouse_pos)

            # Button background
            button_color = COLOR_SHIP if is_hovered else COLOR_GRID
            pygame.draw.rect(self.screen, button_color, button_rect)
            pygame.draw.rect(self.screen, COLOR_TEXT, button_rect, 2)

            # Button text
            text = self.button_font.render(difficulty, True, COLOR_TEXT)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def handle_click(self, pos):
        """
        Handle mouse click on buttons.

        Args:
            pos: Mouse position (x, y)

        Returns:
            Selected difficulty name if a button was clicked, None otherwise
        """
        for difficulty, button_rect in self.buttons:
            if button_rect.collidepoint(pos):
                self.selected_difficulty = difficulty
                return difficulty
        return None

    def run(self):
        """
        Run the start screen loop until a difficulty is selected.

        Returns:
            Selected difficulty name as string
        """
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    difficulty = self.handle_click(event.pos)
                    if difficulty:
                        return difficulty

            self.draw()
            clock.tick(60)  # 60 FPS

        return self.selected_difficulty
