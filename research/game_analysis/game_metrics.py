from statistics import mean

import pandas as pd
from scipy.stats import entropy
from state_analysis import analyze_state_graph
from state_graph import build_state_graph, create_initial_state


def generate_metrics(
    dice_num_values: range,
    side_num_values: range,
) -> pd.DataFrame:

    rows = []

    for num_dice in dice_num_values:
        for num_sides in side_num_values:
            initial = create_initial_state(num_dice, num_sides)

            graph, states_by_depth = build_state_graph(initial)

            analysis = analyze_state_graph(initial, graph)

            for depth in analysis.histories_by_depth:
                # ========== Basic Unweighted Metrics ==========
                rows.append(
                    {
                        "num_dice": num_dice,
                        "num_sides": num_sides,
                        "depth": depth,
                        "num_histories": len(analysis.histories_by_depth[depth]),
                        "num_states": len(states_by_depth[depth]),
                        "avg_states_per_history": mean(
                            len(analysis.states_by_history[depth][history])
                            for history in analysis.states_by_history[depth]
                        ),
                        "max_states_per_history": max(
                            len(analysis.states_by_history[depth][history])
                            for history in analysis.states_by_history[depth]
                        ),
                        "avg_entropy_per_history": mean(
                            entropy(analysis.states_by_history[depth][history].values())
                            for history in analysis.states_by_history[depth]
                        ),
                    }
                )

                # ========== Basic Weighted Metrics ==========

    return pd.DataFrame(rows)
