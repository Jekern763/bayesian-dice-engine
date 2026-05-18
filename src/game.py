from game_state import GameState
from depleting_dice import DepletingDice

class Game:
    def __init__(self, num_peeks:int=4):
        self.die1 = DepletingDice()
        self.die2 = DepletingDice()
        self.state = GameState(current_dice=(self.die1, self.die2))
        self.num_peeks = num_peeks

    def reset(self):
        self.die1.reset()
        self.die2.reset()
        self.state = GameState(current_dice=(self.die1, self.die2))

    def peek(self):
        roll = self.die1.roll() + self.die2.roll()
        self.state.past_rolls.append(roll)
        return roll
    
    def calc_payout(self, guess:int, roll:int) -> float:
        return 0 #insert payout formula here
    
    def guess(self, guess:int):
        roll = self.die1.roll() + self.die2.roll()
        payout = self.calc_payout(guess, roll)
        self.state.net_score += payout
        self.state.past_rolls.append(roll)
        return payout