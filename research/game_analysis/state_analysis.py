from collections import Counter, defaultdict
from dataclasses import dataclass

from analysis_config import Histories, History, StateGraph
from state_graph import GameState


@dataclass
class GraphAnalysis:
    states_by_history: dict[int, dict[History, Counter[GameState]]]
    histories: set[History]
    histories_by_depth: Histories
    history_probabilities: dict[int, dict[History, float]]
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

    # depth -> history -> probability
    history_probabilities: dict[int, dict[History, float]] = defaultdict(
        lambda: defaultdict(float)
    )

    # depth -> state -> possible histories and path counts
    histories_by_state: dict[int, dict[GameState, Counter[History]]] = defaultdict(
        lambda: defaultdict(Counter)
    )

    # All histories at every depth.
    all_histories: set[History] = set()

    # ============================================================
    # Initial state
    # ============================================================

    initial_history: History = ()

    histories_by_state[0][initial_state][initial_history] = 1
    states_by_history[0][initial_history][initial_state] = 1

    histories_by_depth[0].add(initial_history)
    all_histories.add(initial_history)

    # ============================================================
    # Build histories_by_state and states_by_history
    # ============================================================

    for depth in range(num_steps):
        current_states = histories_by_state[depth]
        next_states = histories_by_state[depth + 1]

        for state, histories in current_states.items():
            for transition in state_graph[state]:
                next_state = transition.next_state
                roll = transition.roll

                for history, path_count in histories.items():
                    next_history = history + (roll,)

                    next_states[next_state][next_history] += (
                        path_count * transition.count
                    )

        # Convert the newly generated histories_by_state data into
        # states_by_history for this depth.
        for state, histories in next_states.items():
            for history, path_count in histories.items():
                states_by_history[depth + 1][history][state] += path_count

                histories_by_depth[depth + 1].add(history)
                all_histories.add(history)

    # ============================================================
    # Build history path counts
    # ============================================================

    history_path_counts: dict[History, int] = {
        history: sum(states.values())
        for histories in states_by_history.values()
        for history, states in histories.items()
    }

    # ============================================================
    # Build history probabilities
    # ============================================================

    for depth, histories in states_by_history.items():
        total_paths = sum(sum(states.values()) for states in histories.values())

        for history, states in histories.items():
            history_path_counts_for_history = sum(states.values())

            history_probabilities[depth][history] = (
                history_path_counts_for_history / total_paths
            )

    return GraphAnalysis(
        states_by_history=states_by_history,
        histories=all_histories,
        histories_by_depth=histories_by_depth,
        history_probabilities=history_probabilities,
        histories_by_state=histories_by_state,
        history_path_counts=history_path_counts,
    )
