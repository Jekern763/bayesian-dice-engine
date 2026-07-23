# any graphs that are the same for every algorithm, but do not combine

import ast
from pathlib import Path

import camel_converter
import pandas as pd
import plotly.graph_objects as go
from graph_config import (
    AGENT_COMPARIONS_FIG_DIR,
    ALGORITHM_DFS_BY_GUESS,
    ALGORITHM_DFS_BY_PEEKS,
    ALGORITHM_DFS_BY_ROLL,
    ALGORITHMS,
    FONT_SIZE,
    HEIGHT,
    WIDTH,
)
from graph_utils import save_multi_line

# ========== GRAPHING GUESS FREQUENCY BY GUESS ========== #

fig = go.Figure()

for algorithm in ALGORITHMS:
    df = pd.read_csv(
        f"/Users/jamesekern/pythonProjects/gamblint/research/data/metric_tables/{algorithm}/{algorithm}.csv"
    )

    distribution = ast.literal_eval(df.loc[0, "guess_frequency"])

    guesses = sorted(int(g) for g in distribution.keys())
    frequencies = [
        distribution[str(g)] if str(g) in distribution else distribution[g]
        for g in guesses
    ]

    fig.add_trace(
        go.Scatter(
            x=guesses,
            y=frequencies,
            mode="lines+markers",
            name=(algorithm.replace("_agent", "").replace("_", " ").title()),
        )
    )

fig.update_layout(
    title="Guess Distribution by Algorithm",
    width=WIDTH,
    height=HEIGHT,
    template="simple_white",
    font=dict(size=FONT_SIZE),
    title_font_size=24,
    xaxis_title="Guess",
    yaxis_title="Guess Frequency",
    legend_title_text="Algorithm",
)

fig.update_xaxes(
    dtick=1,
    showgrid=True,
)

fig.update_yaxes(
    showgrid=True,
    rangemode="tozero",
)

output_path = (
    f"{AGENT_COMPARIONS_FIG_DIR}/per_algorithm/guess_distribution_by_algorithm.png"
)

Path(output_path).parent.mkdir(parents=True, exist_ok=True)
fig.write_image(output_path)


# ========== GRAPHING METRCIS BY Guess, Roll, Peeks =========#
condition_dfs = {
    "guess": ALGORITHM_DFS_BY_GUESS,
    "roll": ALGORITHM_DFS_BY_ROLL,
    "peek_average": ALGORITHM_DFS_BY_PEEKS,
}
for condition, dfs in condition_dfs.items():
    graphs = [
        # y_values, graph title)
        "average_payout",
        "exact_hit_rate",
        "mean_absolute_error",
        "average_operations",
    ]

    for y_value in graphs:
        title = f"{y_value.replace('_', ' ').title()} per {condition.title()}"
        save_multi_line(
            dfs,
            condition,
            y_value,
            title,
            condition.replace("_", " ").title(),
            y_value.replace("_", " ").title(),
            f"{AGENT_COMPARIONS_FIG_DIR}/per_algorithm/{camel_converter.to_snake(title)}.png",
        )
