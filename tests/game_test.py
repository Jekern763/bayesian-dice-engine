import pytest
from game_engine.game import Game

@pytest.fixture
def game():
    return Game()

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
    payout = game.guess(7)
    assert game.state.past_rolls[-1] in range(2, 13)

def test_game_payout(game):
    # This test will depend on the payout formula implemented in calc_payout
    # For now, we can just check that the net score is updated correctly
    assert game.calc_payout(7, 7) == 0
    assert game.calc_payout(12, 12) == 0 #TODO: make payout formula and update this test accordingly

def test_game_state_persistence(game):
    for i in range(4): 
        game.peek()
    game.guess(7)
    assert len(game.state.past_rolls) == 5
    # assert game.state.net_score != 0
    # TODO: update this test once payout formula is implemented to check that net_score is updated correctly