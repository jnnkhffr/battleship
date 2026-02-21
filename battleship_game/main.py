"""Main module to run the Battleship game."""

import pygame
from battleship_game.game import BattleshipEasy, BattleshipMedium, BattleshipHard
from battleship_game.screens import StartScreen, GameOverScreen
from battleship_game.config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
)


class GameState:
    SELECTING = 1
    NEW = 2
    RUNNING = 3
    WIN = 4
    LOSS = 5


class GameHandler:
    def __init__(self, game_factories):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Battleship")

        self.clock = pygame.time.Clock()
        self.running = True

        self.game_factories = game_factories
        self.selected_factory = None

        self.start_screen = StartScreen(self.screen, game_factories)
        self.game_over_screen = GameOverScreen(self.screen)

    def run(self):
        current_game = None
        state = GameState.SELECTING

        while self.running:
            events = pygame.event.get()

            if any(e.type == pygame.QUIT for e in events):
                self.running = False
                continue

            if state == GameState.SELECTING:
                selected = self.start_screen.run(events)
                if selected:
                    self.selected_factory = selected(self.screen, self.clock)
                    state = GameState.NEW

            elif state == GameState.NEW:
                current_game = self.selected_factory.create()
                state = GameState.RUNNING

            elif state == GameState.RUNNING:
                still_running = current_game.run(events)
                if not still_running:
                    state = GameState.WIN if current_game.game_over_message == "You win!" else GameState.LOSS

            elif state in (GameState.WIN, GameState.LOSS):
                state = self.game_over_screen.run(state, events)

            self.clock.tick(FPS)

        pygame.quit()


def main():
    handler = GameHandler([BattleshipEasy, BattleshipMedium, BattleshipHard])
    handler.run()


if __name__ == "__main__":
    main()

