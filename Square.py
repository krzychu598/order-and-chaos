import pygame
from constants import (
    SIZE,
    CELL_SIZE,
    CHAOS_SYMBOL,
    ORDER_SYMBOL,
    WIN_CONDITION,
    chaos_image,
    order_image,
    square_image,
)
from functions import check_victory, opponent_move, matrix


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

    def update(self, symbol):
        if self._empty:
            if symbol == ORDER_SYMBOL:
                self.image = order_image
            else:
                self.image = chaos_image

            self._empty = False
            self.update_matrix(symbol)

    def input(self, events, mouse_pos, symbol, game_mode):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(
                mouse_pos
            ):
                self.update(symbol)
                opponent_move(game_mode)
