import pytest
import pygame
from Square import Square
from constants import SIZE, order_image, CELL_SIZE, CIRCLE

# Mocking global variables for testing
pygame.init()
chaos_image = pygame.Surface((CELL_SIZE, CELL_SIZE))
order_image = pygame.Surface((CELL_SIZE, CELL_SIZE))
square_image = pygame.Surface((CELL_SIZE, CELL_SIZE))


@pytest.fixture
def setup_square():
    return Square(0, 0)


def test_square_initialization(setup_square):
    assert setup_square._pos_x == 0
    assert setup_square._pos_y == 0
    assert setup_square._row == 0
    assert setup_square._column == 0
    assert setup_square._empty is True
    assert setup_square._symbol == "empty"


def test_square_is_empty_property(setup_square):
    assert setup_square.is_empty is True
    setup_square._empty = False
    assert setup_square.is_empty is False


def test_square_what_symbol_property(setup_square):
    assert setup_square.what_symbol == "empty"
    setup_square._symbol = CIRCLE
    assert setup_square.what_symbol == CIRCLE
