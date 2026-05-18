from dataclasses import dataclass
from typing import Tuple
from depleting_dice import DepletingDice



@dataclass
class GameState:
    current_dice: Tuple[DepletingDice, DepletingDice]
    net_score: float = 0
    current_round: int = 0

