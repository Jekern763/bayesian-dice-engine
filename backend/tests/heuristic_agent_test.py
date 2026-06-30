import pytest
from agent_algorithms.heuristic_agent import (
    GamblersFallacyAgent,
    InvariantAgent,
    ReflectionAgent,
)


@pytest.fixture
def reflection_agent():
    return ReflectionAgent()


@pytest.fixture
def invariant_agent():
    return InvariantAgent()


@pytest.fixture
def gamblers_fallacy_agent():
    return GamblersFallacyAgent()


def test_all_heuristic_agents_guess_range(
    reflection_agent, invariant_agent, gamblers_fallacy_agent
):
    guess_range = list(range(2, 13))
    assert reflection_agent.simulate_round()["guess"] in guess_range
    assert invariant_agent.simulate_round()["guess"] in guess_range
    assert gamblers_fallacy_agent.simulate_round()["guess"] in guess_range


def test_reflection_agent_guess_strategy(reflection_agent, mocker):
    peeks = [4, 5, 6, 7]
    avg = sum(peeks) / len(peeks)
    reflected_avg = round(14 - avg, 0)
    mock_weighted_random = mocker.patch("agent_algorithms.heuristic_agent.choices")
    mock_weighted_random.return_value = [reflected_avg]
    assert reflection_agent.get_action(peeks) == reflected_avg


def test_invariant_agent_guess_strategy(invariant_agent, mocker):
    peeks = [4, 5, 6, 7]
    remaining = 42 - sum(peeks)
    avg_remaining = round(remaining / 2, 0)
    mock_weighted_random = mocker.patch("agent_algorithms.heuristic_agent.choices")
    mock_weighted_random.return_value = [avg_remaining]
    assert invariant_agent.get_action(peeks) == avg_remaining


def test_gamblers_fallacy_agent_no_repeat_guesses(gamblers_fallacy_agent, mocker):
    peeks = [7, 7, 7, 7]
    mock_random_direction = mocker.patch("agent_algorithms.heuristic_agent.choice")
    mock_weighted_guess = mocker.patch("agent_algorithms.heuristic_agent.choices")
    mock_random_direction.return_value = 1
    mock_weighted_guess.return_value = [7]
    assert gamblers_fallacy_agent.get_action(peeks) == 8
