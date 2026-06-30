import random

from agent_algorithms.agent import Agent


# this algorithm randomly guesses a number between 2 and 12, ignoring the peeks. This is a baseline for testing the game engine and the agent framework. It should perform worse than any algorithm that uses the peeks, but it should still be able to win some rounds by pure luck.
class RandomAgent(Agent):
    def get_action(self, peeks) -> int:
        return random.randint(2, 12)
