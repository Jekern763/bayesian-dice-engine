from agent_algorithms.agent import Agent


class ConstantAgent(Agent):
    def __init__(self, riskiness, jackpot, constant):
        self.constant = constant
        super().__init__(riskiness, jackpot)

    def get_action(self, peeks):
        return self.constant
