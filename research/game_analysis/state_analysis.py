from collections import Counter, defaultdict

from state_graph import (
    GameState,
    initial_state,
    state_graph,
    states_by_depth,
)

type History = tuple[int, ...]

# ============================================================
# Data structures
# ============================================================

# depth -> history -> possible states and path counts
states_by_history: dict[int, dict[History, Counter[GameState]]] = defaultdict(
    lambda: defaultdict(Counter)
)

# depth -> set of possible histories
type Histories = dict[int, set[History]]

histories_by_depth: Histories = defaultdict(set)

# history -> probability of observing that history
history_probabilities: dict[History, float] = defaultdict(float)


# ============================================================
# Build states_by_history
# ============================================================

states_by_history[0][()][initial_state] = 1

for depth in range(len(states_by_depth) - 1):
    current_histories = states_by_history[depth]
    next_histories = states_by_history[depth + 1]

    for history, states in current_histories.items():
        for state, path_count in states.items():
            transitions = state_graph[state]

            for transition in transitions:
                next_history = history + (transition.roll,)

                next_histories[next_history][transition.next_state] += path_count

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
