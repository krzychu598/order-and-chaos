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
    if game_mode == "pvp":
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
    order_or_chaos = get_order_or_chaos()

    class BestMove:
        def __init__(self):
            self.max_symbol_amount = 0
            self.current_symbol = None
            self.current_best_square = None

    best_move = BestMove()

    def decide_best_move(result):
        if result[0]:
            (potential_square, potential_symbol, symbol_amount) = result
            if max(symbol_amount, best_move.max_symbol_amount) == symbol_amount:
                if order_or_chaos == "order":
                    if potential_symbol == CROSS:
                        best_move.current_symbol = CIRCLE
                    else:
                        best_move.current_symbol = CROSS
                else:
                    best_move.current_symbol = potential_symbol
                best_move.current_best_square = potential_square
                best_move.max_symbol_amount = symbol_amount

    # convert square.sprites() list to 2D array square_table
    square_table = []
    start = 0
    for row in range(SIZE):
        square_table.append(list(square.sprites())[start : start + SIZE])
        start += SIZE

    def check_line(line):
        line = list(line)
        circle_squares = cross_squares = 0
        possible_circle = possible_cross = 0
        possible_win = None
        best_square = None
        symbol_amount = None
        can_win = False
        # is it possible to create a line?
        for cell in line:
            if cell.what_symbol == CIRCLE:
                circle_squares += 1
                possible_circle += 1
                possible_cross = 0
            elif cell.what_symbol == CROSS:
                cross_squares += 1
                possible_cross += 1
                possible_circle = 0
            elif cell.what_symbol == "empty":
                possible_circle += 1
                possible_cross += 1
            if possible_circle == TO_WIN or possible_cross == TO_WIN:
                can_win = True

        if can_win:
            if cross_squares > circle_squares:
                possible_win = CROSS
                symbol_amount = cross_squares
            if circle_squares >= cross_squares:
                possible_win = CIRCLE
                symbol_amount = circle_squares
            previous_cell = line[0]
            for cell in line:
                if (
                    cell.what_symbol == "empty"
                    and previous_cell.what_symbol == possible_win
                ):
                    best_square = cell
                    break
                if (
                    cell.what_symbol == possible_win
                    and previous_cell.what_symbol == "empty"
                ):
                    best_square = previous_cell
                    break
                previous_cell = cell

        return best_square, possible_win, symbol_amount

    # check rows
    for row in square_table:
        decide_best_move(check_line(row))

    # check columns
    for column in range(SIZE):
        decide_best_move(
            list(check_line(square_table[row][column] for row in range(SIZE)))
        )

    # check diagonals
    row = column = 0
    for diagonal in range(SIZE):
        # main diagonals
        decide_best_move(
            list(
                check_line(
                    square_table[diagonal + i][i] for i in range(SIZE - diagonal)
                )
            )
        )

        decide_best_move(
            list(
                check_line(
                    square_table[i][diagonal + i] for i in range(SIZE - diagonal)
                )
            )
        )

        # reverse diagonals
        if diagonal <= SIZE - TO_WIN:
            decide_best_move(
                list(
                    check_line(
                        square_table[SIZE - diagonal - 1 - i][i]
                        for i in range(SIZE - diagonal)
                    )
                )
            )

            decide_best_move(
                list(
                    check_line(
                        square_table[SIZE - 1 - i][diagonal + i]
                        for i in range(SIZE - diagonal)
                    )
                )
            )

    if state.order_or_chaos is None:
        raise ValueError("order_or_chaos not set")

    if best_move.current_best_square:
        best_move.current_best_square.update(best_move.current_symbol, player="ai")
    else:
        random_ai_move()
