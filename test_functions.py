import pytest
from functions import StateOfTheGame, check_victory, create_sprites
from constants import CIRCLE, CROSS, TO_WIN, SIZE
from Square import Square


@pytest.fixture
def setup_state():
    return StateOfTheGame()


def test_initial_state(setup_state):
    assert setup_state.symbol == CIRCLE
    assert setup_state.game_mode is None
    assert setup_state.order_or_chaos is None
    assert all(all(cell == 0 for cell in row) for row in setup_state.table)


def test_set_symbol(setup_state):
    setup_state.set_symbol(CROSS)
    assert setup_state.symbol == CROSS


def test_set_game_mode(setup_state):
    setup_state.set_game_mode("pvp")
    assert setup_state.game_mode == "pvp"


def test_set_order_or_chaos(setup_state):
    setup_state.set_order_or_chaos("chaos")
    assert setup_state.order_or_chaos == "chaos"


def test_switch_symbol(setup_state):
    setup_state.switch_symbol()
    assert setup_state.symbol == CROSS
    setup_state.switch_symbol()
    assert setup_state.symbol == CIRCLE
