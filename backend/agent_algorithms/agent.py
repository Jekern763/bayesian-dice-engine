from time import time

from game_engine.game import Game


class Agent:
    def __init__(self):
        self.session = Game(8, 10)  # default values for now, will fine tune later

    def reset_session(self) -> None:
        self.session.reset()

    def simulate_round(self) -> dict:
        peeks = []
        for i in range(self.session.num_peeks):
            peeks.append(self.session.peek())
        start_time = time()
        guess = self.get_action(peeks)
        duration = time() - start_time
        payout = self.session.guess(guess)
        return {"payout": payout, "guess": guess, "peeks": peeks, "duration": duration}

    def get_action(self, peeks) -> int:
        raise NotImplementedError("This method should be implemented by subclasses")
