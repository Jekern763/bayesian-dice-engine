import pytest
from game_engine.depleting_dice import DepletingDice as Dice


@pytest.fixture
def dice():
    return Dice()


def test_dice_len(dice):
    assert len(dice) == 6


def test_dice_roll_range(dice):
    roll = dice.roll()
    assert roll in range(1, 7)


def test_dice_roll(dice, mocker):
    mock_dice_roll = mocker.patch("game_engine.depleting_dice.choice")
    mock_dice_roll.return_value = 3
    assert dice.roll() == 3


def test_dice_roll_removal(dice):
    roll = dice.roll()
    assert roll not in dice.current_sides and len(dice) == 5


def test_dice_reset(dice):
    dice.roll()
    dice.reset()
    assert len(dice) == 6 and all(side in dice.current_sides for side in range(1, 7))


def test_dice_too_many_rolls(dice):
    for _ in range(6):
        dice.roll()
    with pytest.raises(ValueError):
        dice.roll()
