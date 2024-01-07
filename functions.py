import pygame
import random
from constants import CROSS, CIRCLE, SIZE, TO_WIN, square


class StateOfTheGame:
    """
    This class monitors state of different variables in the game
    """

    def __init__(self):
        self.symbol = CIRCLE
        self.game_mode = None
        self.order_or_chaos = None
        self.table = [[0 for _ in range(SIZE)] for row in range(SIZE)]
        self.matrix = [list(row) for row in self.table]

    def set_symbol(self, symbol):
        self.symbol = symbol

    def set_game_mode(self, game_mode):
        self.game_mode = game_mode

    def set_order_or_chaos(self, order_or_chaos):
        self.order_or_chaos = order_or_chaos

    def switch_symbol(self):
        if self.symbol == CIRCLE:
            self.symbol = CROSS
        else:
            self.symbol = CIRCLE

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


def initialize():
    state.__init__()


def set_order_or_chaos(chaos_or_order):
    state.set_order_or_chaos(chaos_or_order)


def set_game_mode(game_mode):
    state.set_game_mode(game_mode)


def switch_symbol():
    state.switch_symbol()


def update_square(mouse_pos):
    for object in square:
        if object.rect.collidepoint(mouse_pos):
            object.update(state.symbol)


def get_symbol():
    return state.symbol


def get_game_mode():
    return state.game_mode


def get_order_or_chaos():
    return state.order_or_chaos


def display_text(screen, text_list, font, x_pos, y_pos):
    """
    Function helps to display text in list format
    """
    for text in text_list:
        if not text:
            y_pos += 30
            continue
        text_surface = font.render(text, True, "Red", "black")
        text_rect = text_surface.get_rect(center=(x_pos, y_pos))
        screen.blit(text_surface, text_rect)
        y_pos += 30


def display_rects(screen, rects_with_text_list, font):
    """
    Function displays choice boxes
    """
    colors = ["blue", "red", "green", "yellow"]
    i = 0
    for rect, text in rects_with_text_list:
        pygame.draw.rect(screen, colors[i], rect)
        text_surface = font.render(text, True, "white")
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        i += 1


def update_matrix(row, column, symbol):
    state.matrix[row][column] = symbol


def check_victory():
    """
    Functions checks if one side has won the game
    """

    def check_line(line):
        circle_squares = cross_squares = 0
        for cell in line:
            if cell == CIRCLE:
                circle_squares += 1
                cross_squares = 0
            elif cell == CROSS:
                cross_squares += 1
                circle_squares = 0
            if circle_squares == TO_WIN or cross_squares == TO_WIN:
                return "order"
        return None

    # check rows
    for row in state.matrix:
        result = check_line(row)
        if result:
            return result

    # check columns
    for column in range(SIZE):
        result = check_line(state.matrix[row][column] for row in range(SIZE))
        if result:
            return result

    # check diagonals
    row = column = 0
    for diagonal in range(SIZE):
        # main diagonals
        result = check_line(
            state.matrix[diagonal + i][i] for i in range(SIZE - diagonal)
        )
        if result:
            return result

        result = check_line(
            state.matrix[i][diagonal + i] for i in range(SIZE - diagonal)
        )
        if result:
            return result

        # reverse diagonals
        if diagonal <= SIZE - TO_WIN:
            result = check_line(
                state.matrix[SIZE - diagonal - 1 - i][i] for i in range(SIZE - diagonal)
            )
            if result:
                return result

            result = check_line(
                state.matrix[SIZE - 1 - i][diagonal + i] for i in range(SIZE - diagonal)
            )
            if result:
                return result

    free_square = [sprite for sprite in square.sprites() if sprite.is_empty]
    if not free_square:
        return "chaos"

    return None


def create_sprites(sprite_class):
    """Create sprites -- displayed squares"""
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


def opponent_move(begin=False):
    """
    Move of the opponent
    """
    if begin == True and state.order_or_chaos == "order":
        return
    game_mode = state.game_mode
    order_or_chaos = state.order_or_chaos
    if game_mode == "pvp":
        # it displays on screen that it is player 2 turn
        pass
    if game_mode == "random_ai":
        random_ai_move()
    if game_mode == "smart_ai":
        smart_ai_move()
    if game_mode is None:
        raise ValueError("Game mode is not set")


def random_ai_move():
    """Move of random ai"""
    free_square = [square for square in square.sprites() if square.is_empty]
    if not free_square:
        return
    object = random.choice(free_square)
    symbol = random.choice([CIRCLE, CROSS])
    object.update(symbol, player="ai")


def smart_ai_move():
    """Move of smart ai"""

    def check_line(line):
        circle_squares = cross_squares = 0
        for cell in line:
            if cell == CIRCLE:
                circle_squares += 1
                cross_squares = 0
            elif cell == CROSS:
                cross_squares += 1
                circle_squares = 0
            if circle_squares == TO_WIN or cross_squares == TO_WIN:
                return "order"
        return None

    # check rows
    for row in state.matrix:
        result = check_line(row)
        if result:
            return result

    # check columns
    for column in range(SIZE):
        result = check_line(state.matrix[row][column] for row in range(SIZE))
        if result:
            return result

    # check diagonals
    row = column = 0
    for diagonal in range(SIZE):
        # main diagonals
        result = check_line(
            state.matrix[diagonal + i][i] for i in range(SIZE - diagonal)
        )
        if result:
            return result

        result = check_line(
            state.matrix[i][diagonal + i] for i in range(SIZE - diagonal)
        )
        if result:
            return result

        # reverse diagonals
        if diagonal <= SIZE - TO_WIN:
            result = check_line(
                state.matrix[SIZE - diagonal - 1 - i][i] for i in range(SIZE - diagonal)
            )
            if result:
                return result

            result = check_line(
                state.matrix[SIZE - 1 - i][diagonal + i] for i in range(SIZE - diagonal)
            )
            if result:
                return result

    free_square = [sprite for sprite in square.sprites() if sprite.is_empty]
    if not free_square:
        return "chaos"
    if state.order_or_chaos == "order":
        # play as chaos
        pass
    elif state.order_or_chaos == "chaos":
        # play as order
        pass
    else:
        raise ValueError("order_or_chaos not set")
