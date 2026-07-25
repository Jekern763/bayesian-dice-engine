import sys
from pathlib import Path

import plotly.express as px
from graph_config import ALGORITHMS

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from metric_generators.algorithm_metrics import AlgorithmMetrics

# =====================================================================
# CHANGE IF NEEDED
# =====================================================================

OUTPUT_DIR = (
    "/Users/jamesekern/pythonProjects/gamblint/research/figures/agent_comparisons/misc"
)

DATA_DIR = "/Users/jamesekern/pythonProjects/gamblint/research/data/raw"

# =====================================================================


def save_heatmap(
    df,
    x,
    y,
    z,
    title,
    x_label,
    y_label,
    color_label,
    filename,
):
    pivot = df.pivot(
        index=y,
        columns=x,
        values=z,
    )

    fig = px.imshow(
        pivot,
        text_auto=".3f",
        color_continuous_scale="Viridis",
        labels={
            "x": x_label,
            "y": y_label,
            "color": color_label,
        },
        title=title,
        aspect="equal",
    )

    fig.update_xaxes(dtick=1)
    fig.update_yaxes(dtick=1)

    fig.write_image(f"{OUTPUT_DIR}/{filename}.png", scale=11)


for algorithm in ALGORITHMS:
    metrics = AlgorithmMetrics(f"{DATA_DIR}/{algorithm}_10000.parquet")

    df = metrics.df

    #
    # One row per (roll, guess) pair
    #
    heatmap_df = df.groupby(["roll", "guess"]).agg(
        frequency=("guess", "size"),
        average_payout=("payout", "mean"),
        average_operations=("total_operations", "mean"),
    )

    heatmap_df["frequency"] /= heatmap_df.groupby(level=0)["frequency"].transform("sum")

    heatmap_df = heatmap_df.reset_index()

    save_heatmap(
        heatmap_df,
        x="roll",
        y="guess",
        z="frequency",
        title=f"{algorithm} Guess Frequency",
        x_label="Actual Roll",
        y_label="Guess",
        color_label="Frequency",
        filename=f"{algorithm}_roll_guess_frequency",
    )

    save_heatmap(
        heatmap_df,
        x="roll",
        y="guess",
        z="average_operations",
        title=f"{algorithm} Average Operations",
        x_label="Actual Roll",
        y_label="Guess",
        color_label="Average Operations",
        filename=f"{algorithm}_roll_guess_average_operations",
    )
