"""Start screen for Battleship game with difficulty selection using factory pattern."""

import pygame
from battleship_game.config import COLOR_BG, COLOR_TEXT, COLOR_SHIP, COLOR_GRID


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
        self.title_font = pygame.font.SysFont(None, 72)
        self.button_font = pygame.font.SysFont(None, 48)
        self.subtitle_font = pygame.font.SysFont(None, 32)
        
        # Selected factory (None until a button is clicked)
        self.selected_factory = None
    
    def _create_buttons(self):
        """
        Create button rectangles for each difficulty level.
        
        Returns:
            List of tuples (factory_class, pygame.Rect)
        """
        buttons = []
        button_width = 200
        button_height = 60
        button_spacing = 20
        
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Calculate starting Y position to center buttons vertically
        total_height = (button_height * len(self.game_factories) + 
                       button_spacing * (len(self.game_factories) - 1))
        start_y = (screen_height - total_height) // 2 + 80
        
        for i, factory_class in enumerate(self.game_factories):
            x = (screen_width - button_width) // 2
            y = start_y + i * (button_height + button_spacing)
            button_rect = pygame.Rect(x, y, button_width, button_height)
            buttons.append((factory_class, button_rect))
        
        return buttons
    
    def draw(self):
        """Draw the start screen with title and buttons."""
        self.screen.fill(COLOR_BG)
        
        screen_width = self.screen.get_width()
        
        # Draw title
        title_text = self.title_font.render("BATTLESHIP", True, COLOR_TEXT)
        title_rect = title_text.get_rect(center=(screen_width // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.subtitle_font.render(
            "Select Difficulty", True, COLOR_SHIP
        )
        subtitle_rect = subtitle_text.get_rect(center=(screen_width // 2, 140))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Create and draw buttons
        buttons = self._create_buttons()
        mouse_pos = pygame.mouse.get_pos()
        
        for factory_class, button_rect in buttons:
            # Check if mouse is hovering over button
            is_hovered = button_rect.collidepoint(mouse_pos)
            
            # Button background
            button_color = COLOR_SHIP if is_hovered else COLOR_GRID
            pygame.draw.rect(self.screen, button_color, button_rect)
            pygame.draw.rect(self.screen, COLOR_TEXT, button_rect, 2)
            
            # Extract difficulty name from class name (e.g., "BattleshipEasy" -> "Easy")
            difficulty_name = factory_class.__name__.replace("Battleship", "")
            
            # Button text
            text = self.button_font.render(difficulty_name, True, COLOR_TEXT)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()
    
    def handle_click(self, pos, events):
        """
        Handle mouse click on buttons.
        
        Args:
            pos: Mouse position (x, y)
            events: List of pygame events
            
        Returns:
            Selected GameFactory class if a button was clicked, None otherwise
        """
        buttons = self._create_buttons()
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for factory_class, button_rect in buttons:
                    if button_rect.collidepoint(event.pos):
                        self.selected_factory = factory_class
                        return factory_class
        return None
    
    def run(self, events: list[pygame.event.Event]):
        """
        Run the start screen for one frame.
        
        Args:
            events: List of pygame events to process
            
        Returns:
            Selected GameFactory class if selected, None otherwise
        """
        self.draw()
        return self.handle_click(pygame.mouse.get_pos(), events)
