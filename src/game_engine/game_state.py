from dataclasses import dataclass, field
from game_engine.depleting_dice import DepletingDice


@dataclass
class GameState:
    current_dice: tuple
    net_score: float = 0
    current_round: int = 0
    past_rolls: list = field(default_factory=list)
