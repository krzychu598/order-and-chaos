import pygame
import random
from constants import CHAOS_SYMBOL, ORDER_SYMBOL, SIZE, WIN_CONDITION, square


class StateOfTheGame:
    def __init__(self):
        self._symbol = ORDER_SYMBOL
        self._game_mode = None
        self._order_or_chaos = None
        self.table = [[0 for _ in range(SIZE)] for row in range(SIZE)]
        self.matrix = [list(row) for row in self.table]

    @property
    def get_symbol(self):
        return self._symbol

    def set_symbol(self, symbol):
        self._symbol = symbol

    @property
    def get_game_mode(self):
        return self._game_mode

    def set_game_mode(self, game_mode):
        self._game_mode = game_mode

    @property
    def get_order_or_chaos(self):
        return self._order_or_chaos

    def set_order_or_chaos(self, order_or_chaos):
        self._order_or_chaos = order_or_chaos

    def switch_symbol(self):
        if self._symbol == ORDER_SYMBOL:
            self._symbol = CHAOS_SYMBOL
        else:
            self._symbol = ORDER_SYMBOL

    def create_sprites(self, sprite_class):
        square.empty()
        row = 0
        column = 0
        for vertical in self.table:
            column = 0
            for rect in vertical:
                self.table[column][row] = sprite_class(row, column)
                object = self.table[column][row]
                square.add(object)
                column += 1
            row += 1


state = StateOfTheGame()


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


def check_victory():
    for row in state.matrix:
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
            cell = state.matrix[row][column]
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
            cell = state.matrix[i][j]
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
                cell = state.matrix[i][j]
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
            cell = state.matrix[i][j]
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
            cell = state.matrix[i][j]
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
    for vertical in state.table:
        column = 0
        for rect in vertical:
            state.table[column][row] = sprite_class(row, column)
            object = state.table[column][row]
            square.add(object)
            column += 1
        row += 1


def opponent_move(game_mode, order_or_chaos):
    if game_mode == "pvp":
        # it displays on screen that it is player 2 turn
        pass
    if game_mode == "random_ai":
        random_ai_move()
    if game_mode == "smart_ai":
        smart_ai_move(order_or_chaos)


def random_ai_move():
    """Move of random ai"""
    free_square = [square for square in square.sprites() if square.is_empty]
    if not free_square:
        return
    object = random.choice(free_square)
    symbol = random.choice([ORDER_SYMBOL, CHAOS_SYMBOL])
    object.update(symbol)


def smart_ai_move(game_mode):
    """Move of smart ai"""
    pass
