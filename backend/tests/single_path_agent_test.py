import pytest
from agent_algorithms.single_path_agent import SinglePathAgent


@pytest.fixture
def agent():
    return SinglePathAgent("Nathaniel")


def test_guess_range(agent):
    return_range = list(range(2, 13))
    assert agent.simulate_round()["guess"] in return_range


def test_single_path_search(agent, mocker):

    def mock_payout(guess, roll):
        if guess == 10:
            return 1000
        return 0

    mock_choice = mocker.patch("agent_algorithms.single_path_agent.choice")
    mock_choice.side_effect = lambda x: x[0]

    mocker.patch.object(agent.session, "calc_payout", side_effect=mock_payout)

    assert agent.get_action([7, 7, 7, 7]) == 10
