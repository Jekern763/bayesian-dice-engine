import pytest
from agent_algorithms.expectimax_agent import ExpectimaxAgent


@pytest.fixture
def agent():
    return ExpectimaxAgent()


# 1. test return range


def test_sim_round_range(agent):
    return_range = list(range(2, 13))
    assert agent.simulate_round()["guess"] in return_range


# 2. test get_face_combos


def test_get_face_combos(agent):
    die1 = list(range(1, 7))
    die2 = list(range(1, 7))
    roll = 3
    assert set(agent.get_face_combos(roll, die1, die2)) == {(1, 2), (2, 1)}


# 3. test max_depth
def test_max_depth_error(agent):
    dice = list(range(1, 7))
    with pytest.raises(RuntimeError):
        agent.get_all_possible_sums([7, 7, 7, 7], dice, dice, 3, 2)
    agent.reset_session()
    with pytest.raises(RuntimeError):
        agent.get_all_possible_sums([7, 7, 7, 7, 7], dice, dice, 0, 3)


# 4. test get_best_value (mock payout formula)


def test_get_best_value(agent, mocker):

    def mock_payout(guess, roll):
        if guess == 10:
            return 1000
        return 0

    mocker.patch.object(agent.session, "calc_payout", side_effect=mock_payout)
    peeks = [4, 5, 6, 7]

    assert agent.get_action(peeks) == 10
