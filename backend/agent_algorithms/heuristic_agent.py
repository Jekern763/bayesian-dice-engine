from agent_algorithms.agent import Agent
from random import choices, choice

"""Three algorithms here: ReflectionAgent and InvariantAgent.
1) ReflectionAgent takes the average of the peeks and reflects them across the mean roll of 7
2) InvariantAgent takes the equation sum(remaining_peeks) = 42 - sum(previous_peeks).
    It then divides the sum(remaining_peeks) by number of remaining peeks.
3) GamblersFallacyAgent is based on the reflection agent, but will not guess a number it saw in the peeks

Both agents will then make a guess based on their expected guess, weighted closer to their expected, and bounded within 1 of the expected
"""


class ReflectionAgent(Agent):
    def __init__(self, name: int, weights=[0.25, 0.5, 0.25]):
        super().__init__(name)
        self.weights = weights

    def get_action(self, peeks):
        avg_peek = sum(peeks) / len(peeks)
        reflected_guess = 14 - avg_peek  # reflect across 7
        options = [reflected_guess - 1, reflected_guess, reflected_guess + 1]
        guess = choices(options, weights=self.weights)[0]
        guess = round(guess, 0)
        return max(2, min(12, guess))  # bound guess between 2 and 12


class InvariantAgent(Agent):
    def __init__(self, name, weights=[0.25, 0.5, 0.25]):
        super().__init__(name)
        self.weights = weights

    def get_action(self, peeks):
        remaining_peeks = 6 - len(peeks)
        expected_guess = (42 - sum(peeks)) / remaining_peeks
        options = [expected_guess - 1, expected_guess, expected_guess + 1]
        guess = choices(options, weights=self.weights)[0]
        guess = round(guess, 0)
        return max(2, min(12, guess))  # bound guess between 2 and 12


class GamblersFallacyAgent(Agent):
    def get_action(self, peeks):
        heuristic_agent = ReflectionAgent("Helper")
        best_guess = heuristic_agent.get_action(peeks)
        direction = choice([1, -1])
        while best_guess in peeks:
            if best_guess == 12 or best_guess == 2:
                direction = direction * -1

            best_guess += 1 * direction
        best_guess = round(best_guess)
        return best_guess
