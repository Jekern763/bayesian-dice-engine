from collections import Counter, defaultdict
from dataclasses import dataclass

from analysis_config import Histories, History, StateGraph
from state_graph import GameState

# ============================================================
# Build analysis structures
# ============================================================


@dataclass
class GraphAnalysis:
    states_by_history: dict[int, dict[History, Counter[GameState]]]
    histories: set[tuple[int, ...]]
    histories_by_depth: Histories
    history_probabilities: dict[History, float]
    histories_by_state: dict[int, dict[GameState, Counter[History]]]
    history_path_counts: dict[History, int]


def analyze_state_graph(
    initial_state: GameState,
    state_graph: StateGraph,
) -> GraphAnalysis:
    num_steps = len(initial_state.dice[0])
    # depth -> history -> possible states and path counts
    states_by_history: dict[int, dict[History, Counter[GameState]]] = defaultdict(
        lambda: defaultdict(Counter)
    )

    # depth -> set of possible histories
    histories_by_depth: Histories = defaultdict(set)

    # history -> probability of observing that history
    history_probabilities: dict[History, float] = defaultdict(float)

    # depth -> state -> possible histories and path counts
    histories_by_state: dict[int, dict[GameState, Counter[History]]] = defaultdict(
        lambda: defaultdict(Counter)
    )

    # ============================================================
    # Build histories_by_state, states_by_history
    # ============================================================

    histories_by_state[0][initial_state][()] = 1
    states_by_history[0][()][initial_state] = 1

    for depth in range(num_steps):
        current_states = histories_by_state[depth]
        next_states = histories_by_state[depth + 1]

        for state, histories in current_states.items():
            for transition in state_graph[state]:
                next_state = transition.next_state
                roll = transition.roll

                for history, path_count in histories.items():
                    next_states[next_state][history + (roll,)] += path_count

        for state, histories in next_states.items():
            for history, path_count in histories.items():
                states_by_history[depth + 1][history][state] += path_count

    history_path_counts: dict[History, int] = {
        history: sum(states.values())
        for histories in states_by_history.values()
        for history, states in histories.items()
    }

    # ============================================================
    # Build histories_by_depth
    # ============================================================

    for depth, histories in states_by_history.items():
        histories_by_depth[depth].update(histories.keys())

    # ============================================================
    # Build history probabilities
    # ============================================================

    for depth, histories in states_by_history.items():
        total_paths = sum(
            count for states in histories.values() for count in states.values()
        )

        for history, states in histories.items():
            history_probabilities[history] = sum(states.values()) / total_paths

    return GraphAnalysis(
        states_by_history,
        histories,
        histories_by_depth,
        history_probabilities,
        histories_by_state,
        history_path_counts,
    )
