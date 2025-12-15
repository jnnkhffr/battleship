import pygame.draw

from battleship_game.config import  BLOCK_SIZE, COLOR_SHIP, COLOR_HIT, COLOR_SUNK


def draw_hit(position_x: int, position_y: int, screen):
    pos_x = BLOCK_SIZE * position_x
    pos_y = BLOCK_SIZE * position_y


    # Draw the cross (two intersecting lines)
    pygame.draw.line(screen, COLOR_HIT, (pos_x + 3, pos_y + 3), (pos_x + BLOCK_SIZE - 3, pos_y + BLOCK_SIZE - 3), 5)  # Horizontal line
    pygame.draw.line(screen, COLOR_HIT, (pos_x + 3, pos_y + BLOCK_SIZE - 3), (pos_x + BLOCK_SIZE - 3, pos_y + 3), 5)  # Vertical line

def draw_sunk(position_x: int, position_y: int, screen):
    pos_x = BLOCK_SIZE * position_x
    pos_y = BLOCK_SIZE * position_y


    # Draw the cross (two intersecting lines)
    pygame.draw.line(screen, COLOR_SUNK, (pos_x + 3, pos_y + 3), (pos_x + BLOCK_SIZE - 3, pos_y + BLOCK_SIZE - 3), 5)  # Horizontal line
    pygame.draw.line(screen, COLOR_SUNK, (pos_x + 3, pos_y + BLOCK_SIZE - 3), (pos_x + BLOCK_SIZE - 3, pos_y + 3), 5)  # Vertical line


def draw_miss(position_x: int, position_y: int, screen):
    # position for cross in the middle of a square
    pos_x = BLOCK_SIZE * position_x + BLOCK_SIZE * 0.5
    pos_y = BLOCK_SIZE * position_y + BLOCK_SIZE * 0.5

    pygame.draw.circle(screen, COLOR_SHIP, (pos_x, pos_y), BLOCK_SIZE * 0.3)