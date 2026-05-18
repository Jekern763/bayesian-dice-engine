from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple
from depleting_dice import DepletingDice

class Status(Enum):
    INACTIVE = auto()
    WAITING = auto()
    ROLLING = auto()
    GUESSING = auto()
    FINISHED = auto()

@dataclass
class GameState:
    current_dice: Tuple[DepletingDice, DepletingDice]
    status: Status = Status.INACTIVE
    net_score: float = 0
    current_round: int = 0

