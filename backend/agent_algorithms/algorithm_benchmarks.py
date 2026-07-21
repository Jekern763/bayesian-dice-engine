from agent_algorithms.average_agent import AverageAgent
from agent_algorithms.benchmark import benchmark
from agent_algorithms.constant_agent import ConstantAgent
from agent_algorithms.expectimax_agent import ExpectimaxAgent
from agent_algorithms.heuristic_agent import (
    GamblersFallacyAgent,
    InvariantAgent,
    ReflectionAgent,
)
from agent_algorithms.random_agent import RandomAgent
from agent_algorithms.single_path_agent import SinglePathAgent

agents = {}
agents["random_agent"] = RandomAgent(1, 1)
agents["reflection_agent"] = ReflectionAgent([0, 1, 0], 1, 1)
agents["invariant_agent"] = InvariantAgent([0, 1, 0], 1, 1)
agents["gamblers_fallacy_agent"] = GamblersFallacyAgent(1, 1)
agents["single_path_agent"] = SinglePathAgent(1, 1)
agents["expectimax_agent"] = ExpectimaxAgent(1, 1)
agents["average_agent"] = AverageAgent(1, 1)


for name, agent in agents.items():
    benchmark(agent, name, 10000)

for i in range(2, 13):
    agent = ConstantAgent(1, 1, i)
    benchmark(agent, f"constant_agent_{i}", 10000)
