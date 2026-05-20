import pytest
from agent_algorithms.agent import Agent
from game_engine.game import Game

@pytest.fixture
def agent():
    return Agent("Igor")

def test_agent_initialization(agent):
    assert agent.name == "Igor"
    assert agent.session is not None
    assert isinstance(agent.session, Game)

def test_agent_reset_session(agent):
    agent.session.peek()
    agent.session.guess(7)
    assert len(agent.session.state.past_rolls) == 2
    agent.reset_session()
    assert len(agent.session.state.past_rolls) == 0

def test_agent_simulate_round_error(agent):
    with pytest.raises(NotImplementedError):
        agent.simulate_round()