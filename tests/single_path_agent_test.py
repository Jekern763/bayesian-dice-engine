import pytest
from agent_algorithms.single_path_agent import SinglePathAgent

@pytest.fixture
def agent():
    return SinglePathAgent("Nathaniel")

