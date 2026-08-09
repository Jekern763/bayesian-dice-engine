from collections import Counter, defaultdict
from itertools import product

from analysis_config import NUM_DICE, NUM_SIDES, GameState, StateGraph, Transition


def create_initial_state(num_dice: int = NUM_DICE, num_sides: int = NUM_SIDES):
    initial_die = tuple(range(1, num_sides + 1))

    return GameState(
        dice=tuple(initial_die for _ in range(num_dice)),
    )


def remove_face(die: tuple[int, ...], index: int) -> tuple[int, ...]:
    return die[:index] + die[index + 1 :]


def get_transitions(state: GameState) -> list[Transition]:
    # Use a dictionary to count identical (roll_sum, next_state) pairs
    transition_counts = Counter()

    for rolls in product(*state.dice):
        next_dice = tuple(
            remove_face(die, die.index(roll)) for die, roll in zip(state.dice, rolls)
        )
        sorted_next_dice = tuple(sorted(next_dice))

        # We don't construct the Transition here yet, just track the raw data
        transition_counts[(sum(rolls), sorted_next_dice)] += 1

    # Build the final unique transitions with their weights
    return [
        Transition(roll=roll_sum, next_state=next_state, weight=count)
        for (roll_sum, next_state), count in transition_counts.items()
    ]


def build_state_graph(
    initial_state: GameState,
) -> tuple[StateGraph, dict[int, set[GameState]]]:
    state_graph: dict[GameState, list[Transition]] = {}
    states_by_depth: dict[int, set[GameState]] = defaultdict(set)

    states_by_depth[0].add(initial_state)

    num_steps = min(len(die) for die in initial_state.dice)

    for depth in range(num_steps):
        for state in states_by_depth[depth]:
            if state not in state_graph:
                state_graph[state] = get_transitions(state)

            for transition in state_graph[state]:
                states_by_depth[depth + 1].add(transition.next_state)

    return state_graph, states_by_depth
