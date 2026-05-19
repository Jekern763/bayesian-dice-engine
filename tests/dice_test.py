import pytest

from src.depleting_dice import DepletingDice as Dice

@pytest.fixture
def dice():
    return Dice()

def test_dice_len ():
    assert len(dice) == 6

def test_dice_roll():
    roll = dice.roll()
    assert roll in range(1, 7)

def test_dice_roll_removal():
    roll = dice.roll()
    assert roll not in dice.current_sides and len(dice) == 5

def test_dice_reset():
    dice.roll()
    dice.reset()
    assert len(dice) == 6 and all(side in dice.current_sides for side in range(1, 7))
