from statistics import mean

from agent_algorithms.agent import Agent


class AverageAgent(Agent):
    def get_action(self, peeks):
        return round(mean(peeks))
