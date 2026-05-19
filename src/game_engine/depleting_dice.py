from random import choice
class DepletingDice:
    def __init__(self, num_sides:int=6):
        self.num_sides = num_sides
        self.current_sides = list(range(1, num_sides+1))

    def __len__(self):
        return len(self.current_sides)
    
    def reset(self):
        self.current_sides = list(range(1, self.num_sides+1))

    def roll(self, remove:bool=True) -> int:
        roll =  choice(self.current_sides)
        self.current_sides.remove(roll)
        return roll