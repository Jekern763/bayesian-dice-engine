from agent_algorithms.random_agent import RandomAgent
import pytest
from random import seed

@pytest.fixture
def random_agent():
    return RandomAgent("Nico")

def test_random_agent_initialization(random_agent):
    assert random_agent.name == "Nico"
    assert random_agent.session is not None

def test_random_agent_get_action(random_agent):
    peeks = [7, 7, 7, 7]
    seed(42)
    guess = random_agent.get_action(peeks)
    assert guess == 12 #Seed should produce a consistent guess