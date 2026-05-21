from agent_algorithms.agent import Agent
from random import choices

"""Two algorithms here: ReflectionAgent and InvariantAgent.
1) ReflectionAgent takes the average of the peeks and reflects them across the mean roll of 7
2) InvariantAgent takes the equation sum(remaining_peeks) = 42 - sum(previous_peeks).
    It then divides the sum(remaining_peeks) by number of remaining peeks.

Both agents will then make a guess based on their expected guess, weighted closer to their expected, and bounded within 1 of the expected
"""

class ReflectionAgent(Agent):
    def __init__(self, weights=[0.25, 0.5, 0.25]):
        super().__init__()
        self.weights = weights
    def get_action(self, peeks):
        avg_peek = sum(peeks) / len(peeks)
        reflected_guess = 14 - avg_peek #reflect across 7
        options = [reflected_guess - 1, reflected_guess, reflected_guess + 1]
        guess = choices(options, weights=self.weights)[0]
        return max(2, min(12, guess)) #bound guess between 2 and 12
    
class InvariantAgent(Agent):
    def __init__(self, weights=[0.25, 0.5, 0.25]):
        super().__init__()
        self.weights = weights
    def get_action(self, peeks):
        remaining_peeks = 6 - len(peeks)
        expected_guess = (42 - sum(peeks)) / remaining_peeks
        options = [expected_guess - 1, expected_guess, expected_guess + 1]
        guess = choices(options, weights=self.weights)[0]
        return max(2, min(12, guess)) #bound guess between 2 and 12