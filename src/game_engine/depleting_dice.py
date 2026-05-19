from random import choice
class DepletingDice:
    def __init__(self, num_sides:int=6):
        self.num_sides = num_sides
        self.current_sides = list(range(1, num_sides+1))

    def __len__(self) -> int:
        return len(self.current_sides)
    
    def __contains__(self, item:int) -> bool:
        return item in self.current_sides
    
    def reset(self) -> None:
        self.current_sides = list(range(1, self.num_sides+1))

    def roll(self, remove:bool=True) -> int:
        if len(self.current_sides) == 0:
            raise ValueError("No more sides left to roll")
        roll =  choice(self.current_sides)
        self.current_sides.remove(roll)
        return roll