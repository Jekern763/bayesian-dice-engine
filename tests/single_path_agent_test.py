import pytest
from agent_algorithms.single_path_agent import SinglePathAgent


@pytest.fixture
def agent():
    return SinglePathAgent("Nathaniel")


def test_guess_range(agent):
    return_range = list(range(2, 13))
    assert agent.simulate_round()["guess"] in return_range


def test_single_path_search(agent, mocker):

    mock_choice = mocker.patch("agent_algorithms.single_path_agent.choice")
    mock_choice.side_effect = lambda x: x[0]

    mock_payout = lambda guess, roll: 1000 if guess == 10 else 0
    mocker.patch.object(agent.session, "calc_payout", side_effect=mock_payout)

    assert agent.get_action([2, 3, 4, 5]) == 10
