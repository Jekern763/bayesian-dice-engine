from random import choice
from json import dumps, loads

class DepletingDice:
    def __init__(self, num_sides: int = 6):
        self.num_sides = num_sides
        self.current_sides = list(range(1, num_sides + 1))

    def __len__(self) -> int:
        return len(self.current_sides)

    def __contains__(self, item: int) -> bool:
        return item in self.current_sides

    def reset(self) -> None:
        self.current_sides = list(range(1, self.num_sides + 1))

    def roll(self, remove: bool = True) -> int:
        if len(self.current_sides) == 0:
            raise ValueError("No more sides left to roll")
        roll = choice(self.current_sides)
        self.current_sides.remove(roll)
        return roll
    
    def to_json(self) -> str:
        state_snapshot = {
            "num_sides": self.num_sides,
            "current_sides": self.current_sides[:]
        }
        return dumps(state_snapshot, indent=4)
    
    @classmethod
    def from_json(cls, json_string: str) -> "DepletingDice":
        state = loads(json_string)
        return cls(
            num_sides=state["num_sides"],
            current_sides=state["current_sides"]
        )
