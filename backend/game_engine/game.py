from game_engine.game_state import GameState
from game_engine.depleting_dice import DepletingDice
from json import loads, dumps
from dataclasses import asdict


class Game:

    def __init__(
        self, 
        riskiness_multiplier: float,
        jackpot_multiplier: float,
        num_peeks: int = 4,
        die1: DepletingDice = None,
        die2: DepletingDice = None
    ) -> None:
        self.riskiness_multiplier = riskiness_multiplier
        self.jackpot_multiplier = jackpot_multiplier
        self.die1 = DepletingDice() if not die1 else die1
        self.die2 = DepletingDice() if not die2 else die2
        self.state = GameState(current_dice=(self.die1, self.die2))
        self.num_peeks = num_peeks

    def reset(self) -> None:
        self.die1.reset()
        self.die2.reset()
        self.state = GameState(current_dice=(self.die1, self.die2))

    def peek(self) -> int:
        roll = self.die1.roll() + self.die2.roll()
        self.state.past_rolls.append(roll)
        return roll

    def calc_payout(self, guess: int, roll: int) -> float:
        if guess == 7:
            return 0.0

        base_stake = (
            self.riskiness_multiplier * self.riskiness_multiplier * abs(guess - 7)
        )
        distance = abs(roll - guess)

        # The Piecewise Jackpot Exception
        if distance == 0:
            return base_stake * self.jackpot_multiplier
        # The Smooth Parabolic Curve

        return (base_stake / 3.0) * (4 - (distance**2))

    def guess(self, guess: int) -> float:
        roll = self.die1.roll() + self.die2.roll()
        payout = self.calc_payout(guess, roll)
        self.state.net_score += payout
        self.state.past_rolls.append(roll)
        return payout

    # Serialization
    def to_json(self) -> str:
        state_snapshot = {
            "riskiness_multiplier": self.riskiness_multiplier,
            "jackpot_multiplier": self.jackpot_multiplier,
            "die1": self.die1.to_json(), #Implement to_json in die1
            "die2": self.die2.to_json(),
            "state": asdict(self.state),
        }
        return dumps(state_snapshot, indent=4)
    
    @classmethod
    def from_json(cls, json_str:str) -> "Game":
        state = loads(json_str)
        instance = cls(
            riskiness_multiplier=state["riskiness_multiplier"],
            jackpot_multiplier=state["jackpot_multiplier"],
            die1=DepletingDice.from_json(state["die1"]),
            die2=DepletingDice.from_json(state["die2"])
        )
        instance.state = GameState(**state["state"])