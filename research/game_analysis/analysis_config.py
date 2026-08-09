from dataclasses import dataclass

# config vars
NUM_SIDES: int = 6
NUM_DICE: int = 2


# dataclasses
@dataclass(
    frozen=True, slots=True
)  # using slots to reduce overhead, prevents creation of dict object
class GameState:
    dice: tuple[tuple[int, ...], ...]


@dataclass(frozen=True, slots=True)
class Transition:
    roll: int
    next_state: GameState
    count: int = 1


# custom types
type StateGraph = dict[GameState, list[Transition]]
type History = tuple[int, ...]
type Histories = dict[int, set[History]]
