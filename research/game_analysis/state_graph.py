from collections import defaultdict
from dataclasses import dataclass

# ============================================================
# Types
# ============================================================


@dataclass(frozen=True)
class GameState:
    die1: tuple[int, ...]
    die2: tuple[int, ...]


@dataclass(frozen=True)
class Transition:
    roll: int
    next_state: GameState


# ============================================================
# Configuration
# ============================================================

num_sides = 6

initial_die = tuple(range(1, num_sides + 1))

initial_state = GameState(
    die1=initial_die,
    die2=initial_die,
)
# ============================================================
# Generate state graph
# ============================================================

state_graph: dict[GameState, set[Transition]] = defaultdict(set)


def get_transitions(state: GameState) -> set[Transition]:
    """
    Generate all possible next states from a given state.
    """

    transitions = set()

    for side1 in state.die1:
        for side2 in state.die2:
            next_state = GameState(
                die1=tuple(x for x in state.die1 if x != side1),
                die2=tuple(x for x in state.die2 if x != side2),
            )

            transitions.add(
                Transition(
                    roll=side1 + side2,
                    next_state=next_state,
                )
            )

    return transitions


states_by_depth: dict[int, set[GameState]] = defaultdict(set)

states_by_depth[0].add(initial_state)


for t in range(num_sides):
    for state in states_by_depth[t]:
        if state not in state_graph:
            state_graph[state].update(get_transitions(state))

        transitions = state_graph[state]

        state_graph[state].update(transitions)

        for transition in transitions:
            states_by_depth[t + 1].add(transition.next_state)
