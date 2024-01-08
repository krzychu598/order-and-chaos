import pygame
from constants import (
    CELL_SIZE,
    CIRCLE,
    chaos_image,
    order_image,
    square_image,
)
from functions import opponent_move, update_matrix


# Square class
class Square(pygame.sprite.Sprite):
    """
    class representing a single square on screen
    """
    global chaos_image, order_image, square_image

    def __init__(self, row, column):
        super().__init__()
        self.image = square_image
        self._pos_x = column * CELL_SIZE
        self._pos_y = row * CELL_SIZE
        self._row = row
        self._column = column
        self.rect = self.image.get_rect(topleft=(column * CELL_SIZE, row * CELL_SIZE))
        self._empty = True
        self._symbol = "empty"

    @property
    def is_empty(self):
        return self._empty
    
    @property
    def what_symbol(self):
        return self._symbol

    def update(self, symbol, player="you"):
        if self._empty:
            if symbol == CIRCLE:
                self.image = order_image
                self._symbol = symbol
            else:
                self.image = chaos_image
                self._symbol = symbol

            self._empty = False
            update_matrix(self._row, self._column, symbol)
            if player == "you":
                opponent_move()
