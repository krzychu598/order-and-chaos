import pygame
import random
from constants import SIZE, CELL_SIZE, CHAOS_SYMBOL, ORDER_SYMBOL, WIN_CONDITION, chaos_image, order_image, square_image

square = pygame.sprite.Group()

def create_sprites():
    """Create sprites"""
    global square
    square.empty()
    row = 0
    column = 0
    for vertical in table:
        column = 0
        for rect in vertical:
            table[column][row] = Square(row, column)
            object = table[column][row]
            square.add(object)
            column += 1
        row += 1


def initialize_matrix():
    global matrix, table
    table = [[0 for _ in range(SIZE)] for row in range(SIZE)]
    matrix = [list(row) for row in table]


def ai_move():
    free_square = [square for square in square.sprites() if square.is_empty]
    if not free_square:
        return
    object = random.choice(free_square)
    symbol = random.choice([ORDER_SYMBOL, CHAOS_SYMBOL])
    object.update(symbol, player="ai")


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
                return "order won"

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
                    return "order won"
                row += 1

    for diagonal in range(SIZE - 1):

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
                return "order won"
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
                    return "order won"
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
                return "order won"
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
                return "order won"
            i -= 1
            j += 1
    
    free_square = [sprite for sprite in square.sprites() if sprite.is_empty]
    if not free_square:
        return "chaos won"
        
    return


# Square class
class Square(pygame.sprite.Sprite):
    global chaos_image, order_image, square_image, matrix

    def __init__(self, row, column):
        super().__init__()
        self.image = square_image
        self._pos_x = column * CELL_SIZE
        self._pos_y = row * CELL_SIZE
        self._row = row
        self._column = column
        self.rect = self.image.get_rect(topleft=(column * CELL_SIZE, row * CELL_SIZE))
        self._empty = True

    @property
    def is_empty(self):
        return self._empty
        

    def update_matrix(self, symbol):
        matrix[self._row][self._column] = symbol

    def update(self, symbol, player):
        if self._empty:
            if symbol == ORDER_SYMBOL:
                self.image = order_image
            else:
                self.image = chaos_image

            self._empty = False
            self.update_matrix(symbol)
            check_victory()


            if player == "player":
                ai_move()

    def input(self, events, mouse_pos, symbol):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos):
                self.update(symbol, player="player")