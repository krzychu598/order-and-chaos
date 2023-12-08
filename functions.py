import pygame
import random
from constants import CHAOS_SYMBOL, ORDER_SYMBOL, SIZE, WIN_CONDITION, square

table = []
matrix = []


def display_text(screen, text_list, font, x_pos, y_pos):
    for text in text_list:
        if not text:
            y_pos += 30
            continue
        text_surface = font.render(text, True, "Red", "black")
        text_rect = text_surface.get_rect(center=(x_pos, y_pos))
        screen.blit(text_surface, text_rect)
        y_pos += 30


def display_rects(screen, rects_with_text_list, font):
    colors = ["green", "blue", "red", "yellow"]
    i = 0
    for rect, text in rects_with_text_list:
        pygame.draw.rect(screen, colors[i], rect)
        text_surface = font.render(text, True, "white")
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        i += 1


def switch_symbol(symbol):
    if symbol == ORDER_SYMBOL:
        symbol = CHAOS_SYMBOL
    else:
        symbol = ORDER_SYMBOL
    return symbol


def check_victory():
    for row in matrix:
        circle_squares = 0
        cross_squares = 0
        for cell in row:
            if cell == ORDER_SYMBOL:
                circle_squares += 1
                cross_squares = 0
            if cell == CHAOS_SYMBOL:
                cross_squares += 1
                circle_squares = 0
            if circle_squares == WIN_CONDITION or cross_squares == WIN_CONDITION:
                return "order"

    for column in range(SIZE):
        row = 0
        circle_squares = 0
        cross_squares = 0
        while row < SIZE:
            cell = matrix[row][column]
            if cell == ORDER_SYMBOL:
                circle_squares += 1
                cross_squares = 0
            if cell == CHAOS_SYMBOL:
                cross_squares += 1
                circle_squares = 0
            if circle_squares == WIN_CONDITION or cross_squares == WIN_CONDITION:
                return "order"
            row += 1

    for diagonal in range(SIZE - WIN_CONDITION + 1):
        circle_squares = 0
        cross_squares = 0
        i = diagonal
        j = 0
        while i < SIZE and j < SIZE:
            cell = matrix[i][j]
            if cell == ORDER_SYMBOL:
                circle_squares += 1
                cross_squares = 0
            if cell == CHAOS_SYMBOL:
                cross_squares += 1
                circle_squares = 0
            if circle_squares == WIN_CONDITION or cross_squares == WIN_CONDITION:
                return "order"
            i += 1
            j += 1

        if diagonal != 0:
            circle_squares = 0
            cross_squares = 0
            i = 0
            j = diagonal
            while i < SIZE and j < SIZE:
                cell = matrix[i][j]
                if cell == ORDER_SYMBOL:
                    circle_squares += 1
                    cross_squares = 0
                if cell == CHAOS_SYMBOL:
                    cross_squares += 1
                    circle_squares = 0
                if circle_squares == WIN_CONDITION or cross_squares == WIN_CONDITION:
                    return "order"
                i += 1
                j += 1

        circle_squares = 0
        cross_squares = 0
        i = SIZE - 1
        j = diagonal
        while i >= 0 and j < SIZE:
            cell = matrix[i][j]
            if cell == ORDER_SYMBOL:
                circle_squares += 1
                cross_squares = 0
            if cell == CHAOS_SYMBOL:
                cross_squares += 1
                circle_squares = 0
            if circle_squares == WIN_CONDITION or cross_squares == WIN_CONDITION:
                return "order"
            i -= 1
            j += 1

        circle_squares = 0
        cross_squares = 0
        i = SIZE - diagonal - 1
        j = 0
        while i >= 0 and j < SIZE:
            cell = matrix[i][j]
            if cell == ORDER_SYMBOL:
                circle_squares += 1
                cross_squares = 0
            if cell == CHAOS_SYMBOL:
                cross_squares += 1
                circle_squares = 0
            if circle_squares == WIN_CONDITION or cross_squares == WIN_CONDITION:
                return "order"
            i -= 1
            j += 1

    free_square = [sprite for sprite in square.sprites() if sprite.is_empty]
    if not free_square:
        return "chaos"

    return


def create_sprites(sprite_class):
    """Create sprites"""
    square.empty()
    row = 0
    column = 0
    for vertical in table:
        column = 0
        for rect in vertical:
            table[column][row] = sprite_class(row, column)
            object = table[column][row]
            square.add(object)
            column += 1
        row += 1


def initialize_matrix():
    global matrix, table
    """Initialize matrix"""
    table += [[0 for _ in range(SIZE)] for row in range(SIZE)]
    matrix += [list(row) for row in table]


def opponent_move(game_mode):
    if game_mode == "pvp":
        # it displays on screen that it is player 2 turn
        pass
    if game_mode == "random_ai":
        random_ai_move()
    if game_mode == "smart_ai":
        smart_ai_move()


def random_ai_move():
    """Move of random ai"""
    free_square = [square for square in square.sprites() if square.is_empty]
    if not free_square:
        return
    object = random.choice(free_square)
    symbol = random.choice([ORDER_SYMBOL, CHAOS_SYMBOL])
    object.update(symbol)


def smart_ai_move():
    """Move of smart ai"""
    pass
