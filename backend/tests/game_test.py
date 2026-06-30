import pytest
from game_engine.game import Game


@pytest.fixture
def game():
    return Game(10, 8)  # basic values for now, will fine tune later


def test_game_initialization(game):
    assert game.state.net_score == 0
    assert game.state.current_round == 0
    assert game.state.past_rolls == []
    assert len(game.die1) == 6
    assert len(game.die2) == 6


def test_game_reset(game):
    game.peek()
    game.guess(7)
    game.reset()
    assert game.state.net_score == 0
    assert game.state.current_round == 0
    assert game.state.past_rolls == []
    assert len(game.die1) == 6
    assert len(game.die2) == 6


def test_game_peek(game):
    roll = game.peek()
    assert roll in range(2, 13)
    assert game.state.past_rolls[-1] == roll


def test_game_guess(game):
    game.guess(7)
    assert game.state.past_rolls[-1] in range(2, 13)


def test_game_payout(game):
    assert game.calc_payout(7, 7) == 0
    assert (
        game.calc_payout(12, 12)
        == 2 * (5 * game.riskiness_multiplier) * game.jackpot_multiplier
    )


def test_game_state_persistence(game):
    for i in range(4):
        game.peek()
    game.guess(9)
    assert len(game.state.past_rolls) == 5
    assert (
        game.state.net_score != 0
        or game.state.past_rolls[-1] == 7
        or game.state.past_rolls[-1] == 11
    )  # payout should be nonzero unless the last roll was 9
